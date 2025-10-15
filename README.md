# 📈 Crypto Trend Detector

**Detector automático de tendencias para criptomonedas usando análisis técnico multi-timeframe**

Herramienta profesional en Python que analiza tendencias de mercado en tiempo real utilizando múltiples indicadores técnicos y temporalidades, ideal para traders de scalping y day trading.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 🎯 Características Principales

- ✅ **Análisis Multi-Timeframe**: Evalúa 4 temporalidades simultáneamente (5m, 15m, 1h, 4h)
- ✅ **Indicadores Técnicos Profesionales**: EMA, RSI, MACD, ADX, ATR
- ✅ **Soporte Multi-Exchange**: Bybit, Binance, OKX, KuCoin y más
- ✅ **Detección Inteligente**: Identifica tendencias alcistas, bajistas o laterales
- ✅ **Consenso Automático**: Genera recomendaciones basadas en múltiples timeframes
- ✅ **Manejo de Monedas Nuevas**: Se adapta a criptos con datos históricos limitados
- ✅ **Búsqueda Inteligente**: Encuentra símbolos automáticamente aunque no uses el formato exacto

---

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/crypto-trend-detector.git
cd crypto-trend-detector
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# Linux/Mac
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

**O instalación manual:**
```bash
pip install ccxt pandas numpy
```

---

## 🚀 Uso Rápido

### Análisis Básico
```bash
python main.py
```

El programa te pedirá el símbolo a analizar:
```
¿Qué moneda quieres analizar? (ejemplo: BTC/USDT o BTCUSDT): ETHUSDT
```

### Formatos de Símbolos Aceptados
- `BTC/USDT` (formato estándar)
- `BTCUSDT` (sin barra)
- `BTC` (busca automáticamente pares con USDT)

---

## 📊 Ejemplo de Salida

```
🚀 INICIANDO DETECTOR DE TENDENCIAS CRYPTO
✅ Conectado a BYBIT
✅ 2734 mercados cargados

✅ Símbolo encontrado: BTC/USDT:USDT

============================================================
📈 ANÁLISIS MULTI-TIMEFRAME: BTC/USDT:USDT
============================================================

⏰ TIMEFRAME: 5m
   Tendencia: 🟢 ALCISTA
   Precio: $42,150.50
   EMA Alineación: 4/5
   MACD: ALCISTA
   RSI: 62.45 (ALCISTA)
   ADX: 28.34 (Fuerza: FUERTE)
   Dirección DI: ALCISTA
   Volatilidad (ATR): 125.4567

⏰ TIMEFRAME: 15m
   Tendencia: 🟢 ALCISTA FUERTE
   Precio: $42,150.50
   EMA Alineación: 5/5
   MACD: ALCISTA
   RSI: 68.21 (ALCISTA)
   ADX: 35.67 (Fuerza: FUERTE)

⏰ TIMEFRAME: 1h
   Tendencia: 🟢 ALCISTA FUERTE
   Precio: $42,145.20
   EMA Alineación: 5/5
   MACD: ALCISTA
   RSI: 71.23 (SOBRECOMPRA)
   ADX: 42.18 (Fuerza: FUERTE)

⏰ TIMEFRAME: 4h
   Tendencia: 🟢 ALCISTA
   Precio: $42,140.80
   EMA Alineación: 4/5
   MACD: ALCISTA
   RSI: 65.89 (ALCISTA)
   ADX: 31.45 (Fuerza: FUERTE)

============================================================
🎯 CONSENSO GENERAL:
   Timeframes analizados: 4
   🟢 Alcista: 4/4 timeframes
   🔴 Bajista: 0/4 timeframes
   🟡 Lateral: 0/4 timeframes

✅ SEÑAL FUERTE: Tendencia ALCISTA dominante
   💡 Acción sugerida: Buscar entradas LONG en retrocesos
============================================================
```

---

## 🔧 Configuración

### Cambiar Exchange
Edita `main.py` en la línea de inicialización:

```python
# Bybit (default)
detector = CryptoTrendDetector(exchange_name='bybit')

# Binance
detector = CryptoTrendDetector(exchange_name='binance')

# OKX
detector = CryptoTrendDetector(exchange_name='okx')

# KuCoin
detector = CryptoTrendDetector(exchange_name='kucoin')
```

### Modificar Timeframes
Edita `crypto_trend_detector.py` en el método `analyze_multiple_timeframes()`:

```python
# Default
timeframes = ['5m', '15m', '1h', '4h']

# Para day trading
timeframes = ['1m', '5m', '15m', '1h']

# Para swing trading
timeframes = ['1h', '4h', '1d', '1w']
```

### Personalizar Indicadores
Los parámetros de indicadores se encuentran en el método `calculate_indicators()`:

```python
# EMAs
df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()
df['ema_21'] = df['close'].ewm(span=21, adjust=False).mean()

# RSI
delta = df['close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()

# Modifica los períodos según tu estrategia
```

---

## 📖 Interpretación de Resultados

### 🟢 Tendencia ALCISTA
- **Señal fuerte**: 75% o más de los timeframes son alcistas
- **Acción**: Buscar entradas LONG en retrocesos a soportes
- **Stop Loss**: Por debajo de EMAs o último mínimo significativo

### 🔴 Tendencia BAJISTA
- **Señal fuerte**: 75% o más de los timeframes son bajistas
- **Acción**: Buscar entradas SHORT en rebotes a resistencias
- **Stop Loss**: Por encima de EMAs o último máximo significativo

### 🟡 Tendencia LATERAL
- **Sin consenso**: Timeframes mixtos o ADX débil (<20)
- **Acción**: Operar rangos o esperar confirmación
- **Estrategia**: Break-out o rebotes en extremos del rango

### Niveles de RSI
- **> 70**: Sobrecompra (posible corrección)
- **50-70**: Alcista saludable
- **30-50**: Bajista saludable
- **< 30**: Sobreventa (posible rebote)

### Fuerza de ADX
- **< 20**: Tend