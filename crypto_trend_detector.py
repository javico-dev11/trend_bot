import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class CryptoTrendDetector:
    """
    Detector de tendencias para criptomonedas usando CCXT
    Identifica tendencias alcistas, bajistas o laterales
    """
    
    def __init__(self, exchange_name='bybit'):
        """
        Inicializa el detector con el exchange deseado
        
        Args:
            exchange_name: Nombre del exchange ('binance', 'bybit', 'okx', etc.)
        """
        try:
            exchange_class = getattr(ccxt, exchange_name)
            self.exchange = exchange_class({
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}  # Para futuros
            })
            print(f"✅ Conectado a {exchange_name.upper()}")
            
            # Cargar mercados
            self.exchange.load_markets()
            print(f"✅ {len(self.exchange.markets)} mercados cargados")
        except Exception as e:
            print(f"❌ Error conectando a {exchange_name}: {e}")
            raise
    
    def normalize_symbol(self, symbol):
        """
        Normaliza el símbolo al formato correcto del exchange
        
        Args:
            symbol: Símbolo ingresado por el usuario
        
        Returns:
            Símbolo normalizado o None si no existe
        """
        # Convertir a mayúsculas
        symbol = symbol.upper().strip()
        
        # Si ya tiene formato correcto (BTC/USDT)
        if '/' in symbol:
            if symbol in self.exchange.markets:
                return symbol
        
        # Si viene sin barra (BTCUSDT, COIAUSDT)
        # Intentar agregar /USDT
        if not '/' in symbol:
            if symbol.endswith('USDT'):
                base = symbol[:-4]
                quote = 'USDT'
            elif symbol.endswith('USD'):
                base = symbol[:-3]
                quote = 'USD'
            else:
                base = symbol
                quote = 'USDT'
            
            formatted = f"{base}/{quote}"
            if formatted in self.exchange.markets:
                return formatted
            
            # Intentar con :USDT (formato Bybit perpetuos)
            formatted_perp = f"{base}/{quote}:{quote}"
            if formatted_perp in self.exchange.markets:
                return formatted_perp
        
        # Buscar coincidencias parciales
        symbol_clean = symbol.replace('/', '').replace(':', '')
        for market in self.exchange.markets:
            market_clean = market.replace('/', '').replace(':', '')
            if market_clean == symbol_clean:
                return market
        
        return None
    
    def search_symbol(self, query):
        """
        Busca símbolos que coincidan con la consulta
        
        Args:
            query: Término de búsqueda
        
        Returns:
            Lista de símbolos encontrados
        """
        query = query.upper().strip()
        matches = []
        
        for symbol in self.exchange.markets:
            if query in symbol:
                market = self.exchange.markets[symbol]
                # Filtrar solo contratos perpetuos o spot con USDT
                if market.get('active', True) and ('USDT' in symbol or 'USD' in symbol):
                    matches.append(symbol)
        
        return sorted(matches)[:10]  # Máximo 10 resultados
    
    def get_open_interest(self, symbol):
        """
        Obtiene el Open Interest actual del contrato
        
        Args:
            symbol: Par de trading
        
        Returns:
            Dict con información de Open Interest o None
        """
        try:
            # Verificar si el exchange soporta OI
            if not hasattr(self.exchange, 'fetch_open_interest'):
                return None
            
            oi_data = self.exchange.fetch_open_interest(symbol)
            return {
                'open_interest': oi_data.get('openInterestAmount', 0),
                'open_interest_value': oi_data.get('openInterestValue', 0),
                'timestamp': oi_data.get('timestamp', None)
            }
        except Exception as e:
            # Algunos exchanges no tienen OI o el símbolo no lo soporta
            return None
    
    def get_open_interest_history(self, symbol, timeframe='1h', limit=100):
        """
        Obtiene histórico de Open Interest
        
        Args:
            symbol: Par de trading
            timeframe: Temporalidad
            limit: Número de datos
        
        Returns:
            DataFrame con histórico de OI o None
        """
        try:
            if not hasattr(self.exchange, 'fetch_open_interest_history'):
                return None
            
            oi_history = self.exchange.fetch_open_interest_history(symbol, timeframe, limit=limit)
            
            df_oi = pd.DataFrame(oi_history)
            if not df_oi.empty and 'timestamp' in df_oi.columns:
                df_oi['timestamp'] = pd.to_datetime(df_oi['timestamp'], unit='ms')
                df_oi.set_index('timestamp', inplace=True)
                return df_oi
            return None
        except Exception as e:
            return None
    
    def get_ohlcv_data(self, symbol='BTC/USDT', timeframe='15m', limit=200):
        """
        Obtiene datos OHLCV del exchange
        
        Args:
            symbol: Par de trading (ej: 'BTC/USDT', 'FORM/USDT')
            timeframe: Temporalidad ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Número de velas a obtener
        
        Returns:
            DataFrame con los datos OHLCV
        """
        try:
            # Normalizar símbolo
            normalized = self.normalize_symbol(symbol)
            if normalized is None:
                print(f"❌ Símbolo '{symbol}' no encontrado")
                print(f"💡 Buscando símbolos similares...")
                matches = self.search_symbol(symbol.split('/')[0] if '/' in symbol else symbol)
                if matches:
                    print(f"   Encontrados: {', '.join(matches[:5])}")
                    print(f"   Usa uno de estos símbolos exactos")
                return None
            
            print(f"📊 Obteniendo datos de {normalized} ({timeframe})...")
            ohlcv = self.exchange.fetch_ohlcv(normalized, timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            print(f"✅ {len(df)} velas obtenidas")
            return df
        
        except Exception as e:
            print(f"❌ Error obteniendo datos: {e}")
            return None
    
    def analyze_open_interest(self, symbol, df_price):
        """
        Analiza el Open Interest en relación con el precio
        
        Args:
            symbol: Par de trading
            df_price: DataFrame con datos de precio
        
        Returns:
            Dict con análisis de OI o None
        """
        try:
            # Obtener OI actual
            oi_current = self.get_open_interest(symbol)
            
            # Obtener histórico de OI
            df_oi = self.get_open_interest_history(symbol, '1h', limit=100)
            
            if df_oi is None or oi_current is None:
                return None
            
            if len(df_oi) < 20:
                return None
            
            # Calcular cambio en OI
            oi_values = df_oi['openInterestAmount'].values if 'openInterestAmount' in df_oi.columns else df_oi['openInterest'].values
            
            oi_current_val = oi_values[-1]
            oi_prev_24h = oi_values[-24] if len(oi_values) >= 24 else oi_values[0]
            oi_change_24h = ((oi_current_val - oi_prev_24h) / oi_prev_24h * 100) if oi_prev_24h > 0 else 0
            
            # Tendencia de OI (últimas 12 horas)
            recent_oi = oi_values[-12:]
            oi_slope = np.polyfit(range(len(recent_oi)), recent_oi, 1)[0]
            
            # Determinar tendencia de OI
            if oi_slope > 0 and oi_change_24h > 5:
                oi_trend = "🟢 CRECIENTE FUERTE"
            elif oi_slope > 0 and oi_change_24h > 0:
                oi_trend = "🟢 CRECIENTE"
            elif oi_slope < 0 and oi_change_24h < -5:
                oi_trend = "🔴 DECRECIENTE FUERTE"
            elif oi_slope < 0 and oi_change_24h < 0:
                oi_trend = "🔴 DECRECIENTE"
            else:
                oi_trend = "🟡 ESTABLE"
            
            # Análisis de divergencias precio vs OI
            price_change_24h = ((df_price['close'].iloc[-1] - df_price['close'].iloc[-24]) / df_price['close'].iloc[-24] * 100) if len(df_price) >= 24 else 0
            
            divergence = "NINGUNA"
            if price_change_24h > 2 and oi_change_24h < -2:
                divergence = "⚠️ BAJISTA (Precio sube, OI baja - Posible techo)"
            elif price_change_24h < -2 and oi_change_24h < -2:
                divergence = "✅ CONFIRMACIÓN BAJISTA (Precio y OI bajan - Cierres de longs)"
            elif price_change_24h < -2 and oi_change_24h > 2:
                divergence = "⚠️ ALCISTA (Precio baja, OI sube - Posible suelo)"
            elif price_change_24h > 2 and oi_change_24h > 2:
                divergence = "✅ CONFIRMACIÓN ALCISTA (Precio y OI suben - Nuevas posiciones)"
            
            return {
                'oi_actual': f"{oi_current_val:,.0f}",
                'oi_cambio_24h': f"{oi_change_24h:+.2f}%",
                'oi_tendencia': oi_trend,
                'divergencia': divergence,
                'interpretacion': self._interpret_oi_signal(oi_trend, divergence, price_change_24h)
            }
            
        except Exception as e:
            return None
    
    def _interpret_oi_signal(self, oi_trend, divergence, price_change):
        """
        Interpreta la señal del Open Interest
        
        Args:
            oi_trend: Tendencia del OI
            divergence: Divergencia precio-OI
            price_change: Cambio de precio 24h
        
        Returns:
            String con interpretación
        """
        if "CONFIRMACIÓN ALCISTA" in divergence:
            return "🚀 Entrada de capital nuevo - Tendencia alcista saludable"
        elif "CONFIRMACIÓN BAJISTA" in divergence:
            return "📉 Cierre de posiciones long - Presión vendedora fuerte"
        elif "Precio sube, OI baja" in divergence:
            return "⚠️ Alerta: Subida sin respaldo - Posible corrección pronto"
        elif "Precio baja, OI sube" in divergence:
            return "💎 Oportunidad: Acumulación en caída - Posible rebote"
        elif "CRECIENTE FUERTE" in oi_trend and price_change > 0:
            return "✅ Alto interés del mercado - Momentum positivo"
        elif "DECRECIENTE FUERTE" in oi_trend:
            return "⚠️ Pérdida de interés - Volatilidad puede disminuir"
        else:
            return "➡️ Sin señales claras de OI"
    
    def calculate_indicators(self, df):
        """
        Calcula indicadores técnicos para identificar tendencias
        
        Args:
            df: DataFrame con datos OHLCV
        
        Returns:
            DataFrame con indicadores añadidos
        """
        # EMAs para tendencia
        df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()
        df['ema_21'] = df['close'].ewm(span=21, adjust=False).mean()
        df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()
        
        # RSI para momentum
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # ATR para volatilidad
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        df['atr'] = true_range.rolling(14).mean()
        
        # ADX para fuerza de tendencia
        plus_dm = df['high'].diff()
        minus_dm = -df['low'].diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        tr14 = true_range.rolling(14).sum()
        plus_di = 100 * (plus_dm.rolling(14).sum() / tr14)
        minus_di = 100 * (minus_dm.rolling(14).sum() / tr14)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        df['adx'] = dx.rolling(14).mean()
        df['plus_di'] = plus_di
        df['minus_di'] = minus_di
        
        return df
    
    def identify_trend(self, df):
        """
        Identifica la tendencia actual basada en múltiples indicadores
        
        Args:
            df: DataFrame con indicadores calculados
        
        Returns:
            Dict con información de la tendencia o None si no hay suficientes datos
        """
        if df is None:
            return None
        
        # Para monedas nuevas, necesitamos al menos 50 velas
        if len(df) < 50:
            print(f"   ⚠️  Solo {len(df)} velas disponibles. Se necesitan al menos 50 para análisis confiable.")
            return None
        
        # Última fila (datos actuales)
        current = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Análisis de EMAs
        ema_score = 0
        if current['close'] > current['ema_9']:
            ema_score += 1
        if current['close'] > current['ema_21']:
            ema_score += 1
        if current['close'] > current['ema_50']:
            ema_score += 1
        if current['ema_9'] > current['ema_21']:
            ema_score += 1
        if current['ema_21'] > current['ema_50']:
            ema_score += 1
        
        # Análisis de MACD
        macd_signal = "NEUTRAL"
        if current['macd'] > current['macd_signal']:
            macd_signal = "ALCISTA"
        elif current['macd'] < current['macd_signal']:
            macd_signal = "BAJISTA"
        
        # Análisis de ADX (fuerza de tendencia)
        adx_strength = "DÉBIL"
        if current['adx'] > 25:
            adx_strength = "FUERTE"
        elif current['adx'] > 20:
            adx_strength = "MODERADA"
        
        # Dirección según DI
        di_direction = "NEUTRAL"
        if current['plus_di'] > current['minus_di']:
            di_direction = "ALCISTA"
        elif current['minus_di'] > current['plus_di']:
            di_direction = "BAJISTA"
        
        # RSI analysis
        rsi_signal = "NEUTRAL"
        if current['rsi'] > 70:
            rsi_signal = "SOBRECOMPRA"
        elif current['rsi'] < 30:
            rsi_signal = "SOBREVENTA"
        elif current['rsi'] > 50:
            rsi_signal = "ALCISTA"
        else:
            rsi_signal = "BAJISTA"
        
        # Determinación de tendencia principal
        if ema_score >= 4 and di_direction == "ALCISTA":
            trend = "🟢 ALCISTA FUERTE"
        elif ema_score >= 3 and di_direction == "ALCISTA":
            trend = "🟢 ALCISTA"
        elif ema_score <= 1 and di_direction == "BAJISTA":
            trend = "🔴 BAJISTA FUERTE"
        elif ema_score <= 2 and di_direction == "BAJISTA":
            trend = "🔴 BAJISTA"
        else:
            trend = "🟡 LATERAL/INDEFINIDA"
        
        return {
            'tendencia': trend,
            'precio_actual': current['close'],
            'ema_score': f"{ema_score}/5",
            'macd': macd_signal,
            'rsi': f"{current['rsi']:.2f} ({rsi_signal})",
            'adx': f"{current['adx']:.2f} (Fuerza: {adx_strength})",
            'di_direccion': di_direction,
            'volatilidad_atr': f"{current['atr']:.4f}",
            'volumen': current['volume']
        }
    
    def analyze_multiple_timeframes(self, symbol='BTC/USDT'):
        """
        Analiza tendencia en múltiples temporalidades
        
        Args:
            symbol: Par de trading
        
        Returns:
            Dict con análisis de cada timeframe
        """
        timeframes = ['5m', '15m', '1h', '4h']
        results = {}
        
        print(f"\n{'='*60}")
        print(f"📈 ANÁLISIS MULTI-TIMEFRAME: {symbol}")
        print(f"{'='*60}\n")
        
        for tf in timeframes:
            try:
                df = self.get_ohlcv_data(symbol, tf, limit=200)
                if df is not None and len(df) > 0:
                    df = self.calculate_indicators(df)
                    trend_info = self.identify_trend(df)
                    
                    print(f"⏰ TIMEFRAME: {tf}")
                    
                    # Solo agregar y mostrar si hay datos suficientes
                    if trend_info is not None:
                        results[tf] = trend_info
                        
                        # Mostrar resultados
                        print(f"   Tendencia: {trend_info['tendencia']}")
                        print(f"   Precio: ${trend_info['precio_actual']:.4f}")
                        print(f"   EMA Alineación: {trend_info['ema_score']}")
                        print(f"   MACD: {trend_info['macd']}")
                        print(f"   RSI: {trend_info['rsi']}")
                        print(f"   ADX: {trend_info['adx']}")
                        print(f"   Dirección DI: {trend_info['di_direccion']}")
                        print(f"   Volatilidad (ATR): {trend_info['volatilidad_atr']}")
                    else:
                        print(f"   ⚠️  Datos insuficientes para análisis confiable (moneda muy nueva)")
                    
                    print()
                    
            except Exception as e:
                print(f"⏰ TIMEFRAME: {tf}")
                print(f"   ⚠️  Error: {e}")
                print()
                continue
        
        # Análisis de Open Interest (solo una vez, no por timeframe)
        print(f"{'='*60}")
        print("📊 ANÁLISIS DE OPEN INTEREST")
        print(f"{'='*60}\n")
        
        # Usar datos de 1h para OI
        df_for_oi = self.get_ohlcv_data(symbol, '1h', limit=100)
        if df_for_oi is not None:
            oi_analysis = self.analyze_open_interest(symbol, df_for_oi)
            if oi_analysis:
                print(f"📈 Open Interest Actual: {oi_analysis['oi_actual']}")
                print(f"   Cambio 24h: {oi_analysis['oi_cambio_24h']}")
                print(f"   Tendencia OI: {oi_analysis['oi_tendencia']}")
                print(f"   Divergencia Precio-OI: {oi_analysis['divergencia']}")
                print(f"   💡 {oi_analysis['interpretacion']}")
            else:
                print("⚠️  Open Interest no disponible para este símbolo/exchange")
        else:
            print("⚠️  No se pudo obtener datos para análisis de OI")
        
        print()
        
        # Consenso general
        print(f"{'='*60}")
        if results:
            self.generate_consensus(results)
        else:
            print("❌ No hay suficientes datos en ningún timeframe para generar análisis")
            print("💡 Esta moneda puede ser demasiado nueva o tener bajo volumen")
        print(f"{'='*60}")
        
        # NUEVO: Análisis de riesgos y recomendación
        print()
        print(f"{'='*60}")
        print("🚨 ANÁLISIS DE RIESGOS Y ALERTAS")
        print(f"{'='*60}\n")
        
        risk_analysis = self.analyze_risk_alerts(results, oi_analysis)
        
        if risk_analysis:
            alerts = risk_analysis['alerts']
            
            # Mostrar alertas por nivel
            if alerts['critico']:
                print("🔴 ALERTAS CRÍTICAS:")
                for alert in alerts['critico']:
                    print(f"   ❌ {alert}")
                print()
            
            if alerts['alto']:
                print("🟠 ALERTAS DE RIESGO ALTO:")
                for alert in alerts['alto']:
                    print(f"   ⚠️  {alert}")
                print()
            
            if alerts['medio']:
                print("🟡 ALERTAS DE RIESGO MEDIO:")
                for alert in alerts['medio']:
                    print(f"   ⚡ {alert}")
                print()
            
            if alerts['bajo']:
                print("🟢 SEÑALES POSITIVAS:")
                for alert in alerts['bajo']:
                    print(f"   ✅ {alert}")
                print()
            
            if not any([alerts['critico'], alerts['alto'], alerts['medio'], alerts['bajo']]):
                print("✅ Sin alertas significativas detectadas")
                print()
            
            # Generar recomendación final
            print(f"{'='*60}")
            print("🎯 RECOMENDACIÓN FINAL DE TRADING")
            print(f"{'='*60}\n")
            
            recommendation = self.generate_trading_recommendation(results, oi_analysis, risk_analysis)
            
            if recommendation:
                print(f"📊 ACCIÓN: {recommendation['action']}")
                print(f"   Razón: {recommendation['reason']}")
                print(f"   Score de riesgo: {recommendation['risk_score']}/16")
                print(f"   Sesgo direccional: {recommendation['bias']}")
                print()
                
                if recommendation['recommendations']:
                    print("💡 RECOMENDACIONES ESPECÍFICAS:")
                    for i, rec in enumerate(recommendation['recommendations'], 1):
                        print(f"   {i}. {rec}")
                print()
        else:
            print("⚠️  No se pudo generar análisis de riesgos")
            print()
        
        print(f"{'='*60}")
        
        return results
    
    def analyze_risk_alerts(self, results, oi_analysis=None):
        """
        Genera alertas de riesgo basadas en múltiples factores
        
        Args:
            results: Dict con resultados de análisis por timeframe
            oi_analysis: Dict con análisis de Open Interest
        
        Returns:
            Dict con alertas y recomendación final
        """
        alerts = {
            'critico': [],
            'alto': [],
            'medio': [],
            'bajo': []
        }
        
        if not results:
            return None
        
        # Obtener datos del timeframe más corto (más actual)
        timeframes_order = ['5m', '15m', '1h', '4h']
        current_tf = None
        for tf in timeframes_order:
            if tf in results and results[tf] is not None:
                current_tf = results[tf]
                break
        
        if current_tf is None:
            return None
        
        # 1. ANÁLISIS DE RSI (Sobrecompra/Sobreventa)
        rsi_critical_count = 0
        rsi_values = []
        
        for tf, data in results.items():
            if data:
                rsi_str = data['rsi']
                try:
                    rsi_val = float(rsi_str.split()[0])
                    rsi_values.append(rsi_val)
                    
                    if rsi_val > 85:
                        rsi_critical_count += 1
                    elif rsi_val < 15:
                        rsi_critical_count += 1
                except:
                    pass
        
        avg_rsi = sum(rsi_values) / len(rsi_values) if rsi_values else 50
        
        if rsi_critical_count >= 3:
            if avg_rsi > 70:
                alerts['critico'].append("RSI > 85 en múltiples timeframes - SOBRECOMPRA EXTREMA")
            else:
                alerts['critico'].append("RSI < 15 en múltiples timeframes - SOBREVENTA EXTREMA")
        elif rsi_critical_count >= 2:
            if avg_rsi > 70:
                alerts['alto'].append("RSI > 80 en varios timeframes - Zona de sobrecompra")
            else:
                alerts['alto'].append("RSI < 20 en varios timeframes - Zona de sobreventa")
        elif avg_rsi > 75:
            alerts['medio'].append("RSI promedio alto (>75) - Precaución en entradas LONG")
        elif avg_rsi < 25:
            alerts['medio'].append("RSI promedio bajo (<25) - Precaución en entradas SHORT")
        
        # 2. ANÁLISIS DE DIVERGENCIA OI vs PRECIO
        if oi_analysis:
            divergencia = oi_analysis.get('divergencia', '')
            
            if "Precio sube, OI baja" in divergencia:
                alerts['alto'].append("Divergencia bajista precio-OI - Subida sin respaldo institucional")
            elif "Precio baja, OI sube" in divergencia:
                alerts['medio'].append("Divergencia alcista precio-OI - Posible acumulación")
            elif "CONFIRMACIÓN BAJISTA" in divergencia:
                alerts['alto'].append("Confirmación bajista OI - Cierre masivo de posiciones long")
            elif "CONFIRMACIÓN ALCISTA" in divergencia:
                alerts['bajo'].append("Confirmación alcista OI - Entrada de capital nuevo")
        
        # 3. ANÁLISIS DE VOLATILIDAD (ATR)
        try:
            atr_str = current_tf.get('volatilidad_atr', '0')
            precio_str = current_tf.get('precio_actual', 0)
            
            atr_val = float(atr_str)
            precio_val = float(precio_str)
            
            if precio_val > 0:
                atr_percentage = (atr_val / precio_val) * 100
                
                if atr_percentage > 5:
                    alerts['alto'].append(f"Volatilidad muy alta (ATR {atr_percentage:.2f}% del precio) - Riesgo de gaps")
                elif atr_percentage > 3:
                    alerts['medio'].append(f"Volatilidad elevada (ATR {atr_percentage:.2f}%) - Usar stops amplios")
        except:
            pass
        
        # 4. ANÁLISIS DE FUERZA DE TENDENCIA (ADX)
        try:
            adx_str = current_tf.get('adx', '0')
            adx_val = float(adx_str.split()[0])
            
            if adx_val < 20:
                alerts['medio'].append("ADX débil (<20) - Mercado lateral, evitar trading direccional")
            elif adx_val > 60:
                alerts['alto'].append("ADX muy fuerte (>60) - Tendencia agotada, posible reversión")
        except:
            pass
        
        # 5. ANÁLISIS DE CONSENSO ENTRE TIMEFRAMES
        alcista_count = 0
        bajista_count = 0
        
        for tf, data in results.items():
            if data:
                trend = data.get('tendencia', '')
                if 'ALCISTA' in trend:
                    alcista_count += 1
                elif 'BAJISTA' in trend:
                    bajista_count += 1
        
        total = len([d for d in results.values() if d is not None])
        
        if total >= 3:
            if alcista_count == total or bajista_count == total:
                alerts['bajo'].append(f"Consenso perfecto ({total}/{total} TFs) - Alta probabilidad de continuación")
            elif abs(alcista_count - bajista_count) <= 1 and total >= 3:
                alerts['alto'].append("Sin consenso claro entre timeframes - Mercado indeciso")
        
        # 6. ANÁLISIS COMBINADO (Lo más importante)
        # Detectar "trampa alcista" o "trampa bajista"
        if avg_rsi > 80 and "Precio sube, OI baja" in str(oi_analysis):
            alerts['critico'].append("⚠️ TRAMPA ALCISTA DETECTADA - Probable corrección inminente")
        elif avg_rsi < 20 and "Precio baja, OI baja" in str(oi_analysis):
            alerts['medio'].append("💎 Posible capitulación - Oportunidad de compra en formación")
        
        return {
            'alerts': alerts,
            'avg_rsi': avg_rsi,
            'timeframes_analyzed': total,
            'consensus': 'alcista' if alcista_count > bajista_count else 'bajista' if bajista_count > alcista_count else 'neutral'
        }
    
    def calculate_price_levels(self, df, current_price, trend_direction, atr):
        """
        Calcula niveles de precio para entrada, stop loss y take profit
        
        Args:
            df: DataFrame con datos OHLCV e indicadores
            current_price: Precio actual
            trend_direction: 'alcista', 'bajista' o 'neutral'
            atr: Average True Range
        
        Returns:
            Dict con niveles de precio sugeridos
        """
        if df is None or len(df) < 50:
            return None
        
        try:
            # Obtener EMAs y datos recientes
            ema_9 = df['ema_9'].iloc[-1]
            ema_21 = df['ema_21'].iloc[-1]
            ema_50 = df['ema_50'].iloc[-1]
            
            # Calcular soportes y resistencias (últimas 50 velas)
            recent_data = df.tail(50)
            highs = recent_data['high'].values
            lows = recent_data['low'].values
            
            # Resistencias (máximos significativos)
            resistance_1 = np.percentile(highs, 90)
            resistance_2 = np.percentile(highs, 95)
            resistance_3 = max(highs)
            
            # Soportes (mínimos significativos)
            support_1 = np.percentile(lows, 10)
            support_2 = np.percentile(lows, 5)
            support_3 = min(lows)
            
            levels = {}
            
            if trend_direction == 'alcista':
                # LONG Setup
                # Entrada: Retroceso a EMA21 o 50% del último impulso
                last_low = min(recent_data['low'].tail(10))
                fibonacci_50 = current_price - ((current_price - last_low) * 0.5)
                fibonacci_618 = current_price - ((current_price - last_low) * 0.618)
                
                entry_1 = min(ema_21, fibonacci_50)
                entry_2 = min(ema_50, fibonacci_618)
                
                # Stop Loss: Por debajo de último mínimo o 2x ATR
                stop_loss = max(last_low - atr * 0.5, current_price - atr * 2)
                
                # Take Profit: Basado en resistencias y ATR
                tp1 = current_price + (current_price - stop_loss) * 1.5  # R:R 1.5:1
                tp2 = current_price + (current_price - stop_loss) * 2.5  # R:R 2.5:1
                tp3 = min(resistance_1, current_price + (current_price - stop_loss) * 4)  # R:R 4:1
                
                levels = {
                    'tipo': 'LONG',
                    'precio_actual': current_price,
                    'entradas': {
                        'agresiva': current_price,
                        'moderada': entry_1,
                        'conservadora': entry_2
                    },
                    'stop_loss': stop_loss,
                    'take_profits': {
                        'tp1': tp1,
                        'tp2': tp2,
                        'tp3': tp3
                    },
                    'resistencias': [resistance_1, resistance_2, resistance_3],
                    'soportes': [support_1, support_2, support_3],
                    'riesgo_recompensa': {
                        'tp1': round((tp1 - current_price) / (current_price - stop_loss), 2),
                        'tp2': round((tp2 - current_price) / (current_price - stop_loss), 2),
                        'tp3': round((tp3 - current_price) / (current_price - stop_loss), 2)
                    }
                }
                
            elif trend_direction == 'bajista':
                # SHORT Setup
                # Entrada: Rebote a EMA21 o 50% del último impulso
                last_high = max(recent_data['high'].tail(10))
                fibonacci_50 = current_price + ((last_high - current_price) * 0.5)
                fibonacci_618 = current_price + ((last_high - current_price) * 0.618)
                
                entry_1 = max(ema_21, fibonacci_50)
                entry_2 = max(ema_50, fibonacci_618)
                
                # Stop Loss: Por encima de último máximo o 2x ATR
                stop_loss = min(last_high + atr * 0.5, current_price + atr * 2)
                
                # Take Profit: Basado en soportes y ATR
                tp1 = current_price - (stop_loss - current_price) * 1.5  # R:R 1.5:1
                tp2 = current_price - (stop_loss - current_price) * 2.5  # R:R 2.5:1
                tp3 = max(support_1, current_price - (stop_loss - current_price) * 4)  # R:R 4:1
                
                levels = {
                    'tipo': 'SHORT',
                    'precio_actual': current_price,
                    'entradas': {
                        'agresiva': current_price,
                        'moderada': entry_1,
                        'conservadora': entry_2
                    },
                    'stop_loss': stop_loss,
                    'take_profits': {
                        'tp1': tp1,
                        'tp2': tp2,
                        'tp3': tp3
                    },
                    'resistencias': [resistance_1, resistance_2, resistance_3],
                    'soportes': [support_1, support_2, support_3],
                    'riesgo_recompensa': {
                        'tp1': round((current_price - tp1) / (stop_loss - current_price), 2),
                        'tp2': round((current_price - tp2) / (stop_loss - current_price), 2),
                        'tp3': round((current_price - tp3) / (stop_loss - current_price), 2)
                    }
                }
            else:
                # Neutral - Niveles de rango
                levels = {
                    'tipo': 'RANGO',
                    'precio_actual': current_price,
                    'resistencias': [resistance_1, resistance_2, resistance_3],
                    'soportes': [support_1, support_2, support_3],
                    'recomendacion': 'Comprar en soportes, vender en resistencias'
                }
            
            return levels
            
        except Exception as e:
            return None
    
    def generate_trading_recommendation(self, results, oi_analysis, risk_alerts):
        """
        Genera recomendación final de trading basada en todo el análisis
        
        Args:
            results: Resultados del análisis multi-timeframe
            oi_analysis: Análisis de Open Interest
            risk_alerts: Alertas de riesgo
        
        Returns:
            Dict con recomendación detallada
        """
        if not risk_alerts:
            return None
        
        alerts = risk_alerts['alerts']
        avg_rsi = risk_alerts['avg_rsi']
        consensus = risk_alerts['consensus']
        
        # Calcular nivel de riesgo total
        risk_score = len(alerts['critico']) * 4 + len(alerts['alto']) * 3 + len(alerts['medio']) * 2 + len(alerts['bajo']) * 1
        
        # Determinar acción recomendada
        if risk_score >= 10:
            action = "🛑 NO OPERAR"
            reason = "Riesgo extremadamente alto detectado"
            bias = "NEUTRAL - Esperar confirmación"
        elif risk_score >= 7:
            action = "⚠️ EXTREMA PRECAUCIÓN"
            reason = "Múltiples señales de alerta presentes"
            if consensus == 'alcista' and avg_rsi > 75:
                bias = "SHORT (contrarian) o FUERA DEL MERCADO"
            elif consensus == 'bajista' and avg_rsi < 25:
                bias = "LONG (contrarian) o FUERA DEL MERCADO"
            else:
                bias = "NEUTRAL - Reducir exposición"
        elif risk_score >= 4:
            action = "⚡ OPERAR CON CAUTELA"
            reason = "Algunas señales de alerta detectadas"
            if consensus == 'alcista':
                bias = "LONG en retrocesos - Reducir tamaño de posición"
            elif consensus == 'bajista':
                bias = "SHORT en rebotes - Reducir tamaño de posición"
            else:
                bias = "Esperar setup claro"
        else:
            action = "✅ CONDICIONES FAVORABLES"
            reason = "Pocas alertas de riesgo"
            if consensus == 'alcista':
                bias = "LONG - Buscar entradas en soporte"
            elif consensus == 'bajista':
                bias = "SHORT - Buscar entradas en resistencia"
            else:
                bias = "Operar rangos o breakouts"
        
        # Recomendaciones específicas
        recommendations = []
        
        if avg_rsi > 80:
            recommendations.append("Evitar LONG nuevos - Precio en zona extrema")
            recommendations.append("Considerar tomar ganancias parciales si estás en LONG")
            recommendations.append("SHORT solo con confirmación fuerte y stop ajustado")
        elif avg_rsi < 20:
            recommendations.append("Evitar SHORT nuevos - Precio en zona extrema")
            recommendations.append("Buscar señales de reversión para LONG")
            recommendations.append("Esperar rebote técnico")
        elif consensus == 'alcista' and risk_score < 5:
            recommendations.append("Entrar LONG en retrocesos a EMAs")
            recommendations.append("Stop loss por debajo de último mínimo")
            recommendations.append("Tomar ganancias parciales en resistencias")
        elif consensus == 'bajista' and risk_score < 5:
            recommendations.append("Entrar SHORT en rebotes a EMAs")
            recommendations.append("Stop loss por encima de último máximo")
            recommendations.append("Tomar ganancias parciales en soportes")
        
        # Advertencia especial si hay divergencia OI
        if oi_analysis and "Precio sube, OI baja" in oi_analysis.get('divergencia', ''):
            recommendations.append("⚠️ CRÍTICO: No confiar en esta subida - OI bajando")
            recommendations.append("Preparar salida o considerar cobertura SHORT")
        
        return {
            'action': action,
            'reason': reason,
            'bias': bias,
            'risk_score': risk_score,
            'recommendations': recommendations
        }
    
    def generate_consensus(self, results):
        """
        Genera un consenso basado en todos los timeframes
        
        Args:
            results: Dict con resultados de cada timeframe
        """
        if not results:
            print("❌ No hay datos suficientes para consenso")
            return
        
        alcista_count = 0
        bajista_count = 0
        lateral_count = 0
        
        # Filtrar solo resultados válidos (no None)
        valid_results = {tf: data for tf, data in results.items() if data is not None}
        
        if not valid_results:
            print("❌ No hay análisis válidos para generar consenso")
            return
        
        for tf, data in valid_results.items():
            trend = data['tendencia']
            if 'ALCISTA' in trend:
                alcista_count += 1
            elif 'BAJISTA' in trend:
                bajista_count += 1
            else:
                lateral_count += 1
        
        total = len(valid_results)
        
        print("🎯 CONSENSO GENERAL:")
        print(f"   Timeframes analizados: {total}")
        print(f"   🟢 Alcista: {alcista_count}/{total} timeframes")
        print(f"   🔴 Bajista: {bajista_count}/{total} timeframes")
        print(f"   🟡 Lateral: {lateral_count}/{total} timeframes")
        print()
        
        if total == 0:
            print("⚠️  No hay suficientes datos para recomendación")
            return
        
        if alcista_count >= total * 0.75:
            print("✅ SEÑAL FUERTE: Tendencia ALCISTA dominante")
            print("   💡 Acción sugerida: Buscar entradas LONG en retrocesos")
        elif bajista_count >= total * 0.75:
            print("✅ SEÑAL FUERTE: Tendencia BAJISTA dominante")
            print("   💡 Acción sugerida: Buscar entradas SHORT en rebotes")
        elif alcista_count > bajista_count:
            print("⚠️  SEÑAL MODERADA: Tendencia ALCISTA con cautela")
            print("   💡 Acción sugerida: Preferir LONG, confirmar en timeframe menor")
        elif bajista_count > alcista_count:
            print("⚠️  SEÑAL MODERADA: Tendencia BAJISTA con cautela")
            print("   💡 Acción sugerida: Preferir SHORT, confirmar en timeframe menor")
        else:
            print("🟡 SIN CONSENSO: Mercado lateral o indefinido")
            print("   💡 Acción sugerida: Esperar confirmación clara, operar rangos")
