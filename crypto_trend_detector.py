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
        
        # Consenso general
        print(f"{'='*60}")
        if results:
            self.generate_consensus(results)
        else:
            print("❌ No hay suficientes datos en ningún timeframe para generar análisis")
            print("💡 Esta moneda puede ser demasiado nueva o tener bajo volumen")
        print(f"{'='*60}")
        
        return results
    
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

