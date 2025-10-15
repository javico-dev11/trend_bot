# 📈 Crypto Trend Detector

**Detector automático de tendencias para criptomonedas usando análisis técnico multi-timeframe**

Herramienta profesional en Python que analiza tendencias de mercado en tiempo real utilizando múltiples indicadores técnicos y temporalidades, ideal para traders de scalping y day trading.

**🆕 NUEVO: Bot de Telegram integrado - Consulta análisis desde tu celular 24/7!**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Telegram](https://img.shields.io/badge/telegram-bot-blue.svg)

---

## 🎯 Características Principales

- ✅ **Análisis Multi-Timeframe**: Evalúa 4 temporalidades simultáneamente (5m, 15m, 1h, 4h)
- ✅ **Indicadores Técnicos Profesionales**: EMA, RSI, MACD, ADX, ATR
- ✅ **Open Interest Analysis**: Detecta divergencias precio-OI
- ✅ **Sistema de Alertas**: Identifica riesgos críticos automáticamente
- ✅ **Niveles de Precio**: Entrada, Stop Loss y Take Profit calculados
- ✅ **Soporte Multi-Exchange**: Bybit, Binance, OKX, KuCoin y más
- 🤖 **Bot de Telegram**: Consulta análisis desde cualquier lugar
- ✅ **Detección de Trampas**: Identifica "bull traps" y "bear traps"
- ✅ **Recomendaciones Inteligentes**: Basadas en análisis de riesgo

---

## 🚀 Modos de Uso

### 1. 💻 Modo Terminal (Análisis Individual)
```bash
python main.py
```

### 2. 🤖 Modo Bot de Telegram (24/7)
```bash
python telegram_bot.py
```
**Consulta análisis desde Telegram:**
- `/analizar BTCUSDT` - Análisis completo
- `/quick ETHUSDT` - Análisis rápido
- `/precio BTCUSDT` - Ver precio actual

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
- **< 20**: Tendencia débil o lateral
- **20-25**: Tendencia moderada
- **> 25**: Tendencia fuerte

---

## 📁 Estructura del Proyecto

```
crypto-trend-detector/
│
├── main.py                      # Script principal ejecutable
├── crypto_trend_detector.py     # Clase principal con toda la lógica
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Este archivo
│
├── myenv/                       # Entorno virtual (no incluir en git)
│
└── .gitignore                   # Archivos a ignorar en git
```

---

## 🛠️ API de la Clase Principal

### `CryptoTrendDetector`

#### Constructor
```python
detector = CryptoTrendDetector(exchange_name='bybit')
```

#### Métodos Principales

**`get_ohlcv_data(symbol, timeframe, limit)`**
```python
df = detector.get_ohlcv_data('BTC/USDT', '15m', limit=200)
# Retorna: DataFrame con OHLCV data
```

**`calculate_indicators(df)`**
```python
df_with_indicators = detector.calculate_indicators(df)
# Retorna: DataFrame con EMAs, RSI, MACD, ADX, ATR
```

**`identify_trend(df)`**
```python
trend_info = detector.identify_trend(df)
# Retorna: Dict con análisis completo de tendencia
```

**`analyze_multiple_timeframes(symbol)`**
```python
results = detector.analyze_multiple_timeframes('ETH/USDT')
# Retorna: Dict con análisis de cada timeframe
```

---

## 💡 Casos de Uso

### 1. Scalping (5m - 15m)
```python
# Buscar alineación de EMAs en 5m
# Confirmar con 15m antes de entrar
# RSI entre 40-60 para entradas
# ADX > 25 para confirmar fuerza
```

### 2. Day Trading (15m - 1h)
```python
# Tendencia principal en 1h
# Entradas en 15m en retrocesos
# MACD como confirmación adicional
# Stop loss basado en ATR
```

### 3. Swing Trading (1h - 4h - 1d)
```python
# Dirección en 1d
# Setup en 4h
# Entrada precisa en 1h
# Targets en resistencias mayores
```

---

## ⚠️ Limitaciones y Consideraciones

### Monedas Nuevas
- Criptos recién listadas pueden tener menos de 50 velas en timeframes grandes
- El sistema se adapta automáticamente y analiza solo los timeframes disponibles
- Mensaje informativo: `⚠️ Datos insuficientes para análisis confiable`

### Rate Limits
- Los exchanges tienen límites de peticiones por minuto
- CCXT maneja esto automáticamente con `enableRateLimit: True`
- Para análisis masivos, considera implementar delays

### Datos en Tiempo Real
- Los datos tienen un retraso de ~1 segundo
- Para trading de alta frecuencia, considera WebSockets

---

## 🔐 Seguridad

### API Keys (Para funciones avanzadas)
Si planeas implementar trading automático:

```python
exchange = ccxt.bybit({
    'apiKey': 'TU_API_KEY',
    'secret': 'TU_SECRET',
    'enableRateLimit': True,
})
```

**⚠️ IMPORTANTE:**
- Nunca compartas tus API keys
- Usa archivos `.env` para credenciales
- Activa solo permisos de lectura si no vas a operar
- Limita IPs de acceso en el exchange

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ideas para Contribuir
- [ ] Soporte para más indicadores (Bollinger Bands, Ichimoku)
- [ ] Exportar análisis a CSV/JSON
- [ ] Alertas por Telegram/Discord
- [ ] Dashboard web con Streamlit
- [ ] Backtesting histórico
- [ ] Machine Learning para predicciones

---

## 📝 Changelog

### v1.0.0 (2025-01-15)
- ✅ Análisis multi-timeframe inicial
- ✅ Soporte para 7 indicadores técnicos
- ✅ Compatibilidad con múltiples exchanges
- ✅ Manejo robusto de monedas nuevas
- ✅ Búsqueda inteligente de símbolos

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## ⚡ Roadmap

- [ ] **v1.1**: Alertas automáticas por Telegram
- [ ] **v1.2**: Dashboard web interactivo
- [ ] **v1.3**: Backtesting engine
- [ ] **v1.4**: Machine Learning integration
- [ ] **v2.0**: Trading bot automático (con aprobación manual)

---

## 📞 Soporte

¿Problemas o preguntas?

- 📧 Email: tu-email@ejemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/crypto-trend-detector/issues)
- 💬 Telegram: @tu_usuario

---

## ⚖️ Disclaimer

**ADVERTENCIA**: Esta herramienta es solo para fines educativos e informativos. 

- ❌ No es asesoramiento financiero
- ❌ El trading de criptomonedas conlleva riesgos significativos
- ❌ Puedes perder todo tu capital
- ✅ Siempre practica primero en cuentas demo
- ✅ Nunca inviertas más de lo que puedas permitirte perder
- ✅ Investiga y forma tu propia estrategia

El autor no se hace responsable de pérdidas financieras derivadas del uso de esta herramienta.

---

## 🌟 Agradecimientos

- [CCXT](https://github.com/ccxt/ccxt) - Librería increíble para conectar exchanges
- [Pandas](https://pandas.pydata.org/) - Análisis de datos en Python
- [NumPy](https://numpy.org/) - Computación numérica
- Comunidad de traders que comparten conocimiento abiertamente

---

**Hecho con ❤️ para la comunidad de traders**

*"El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora." - Proverbio chino*

---

### 🚀 Quick Start
```bash
git clone https://github.com/tu-usuario/crypto-trend-detector.git
cd crypto-trend-detector
python -m venv myenv
source myenv/bin/activate  # En Windows: myenv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**¡Empieza a analizar el mercado en menos de 2 minutos!** 📈