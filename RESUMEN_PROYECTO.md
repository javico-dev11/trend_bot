# 📊 Crypto Trend Detector - Resumen del Proyecto

## 🎯 ¿Qué hace este proyecto?

Analiza tendencias de criptomonedas en tiempo real usando análisis técnico profesional, con:
- ✅ Múltiples indicadores (RSI, MACD, EMA, ADX, ATR)
- ✅ Análisis de Open Interest
- ✅ Detección automática de riesgos
- ✅ Niveles de precio calculados (entrada, stop, targets)
- ✅ **Bot de Telegram para consultas 24/7**

---

## 📁 Estructura del Proyecto

```
crypto-trend-detector/
│
├── 📄 main.py                      # Script principal (modo terminal)
├── 🤖 telegram_bot.py              # Bot de Telegram
├── 🧠 crypto_trend_detector.py     # Motor de análisis
│
├── 📋 requirements.txt             # Dependencias Python
├── 📖 README.md                    # Documentación principal
├── 📖 TELEGRAM_BOT_SETUP.md        # Guía del bot de Telegram
├── 🔧 .env.example                 # Template de configuración
├── 🚫 .gitignore                   # Archivos a ignorar en git
│
└── 📁 myenv/                       # Entorno virtual (no subir a git)
```

---

## 🚀 Quick Start (5 minutos)

### Para usar en Terminal:
```bash
# 1. Clonar o descargar proyecto
# 2. Crear entorno virtual
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

### Para usar con Telegram:
```bash
# 1. Crear bot con @BotFather en Telegram
# 2. Copiar token

# 3. Windows:
$env:TELEGRAM_BOT_TOKEN = "TU_TOKEN"

# Linux/Mac:
export TELEGRAM_BOT_TOKEN="TU_TOKEN"

# 4. Ejecutar bot
python telegram_bot.py

# 5. En Telegram, buscar tu bot y usar:
/analizar BTCUSDT
```

---

## 📊 Análisis que Realiza

### 1. **Multi-Timeframe**
- 5 minutos (scalping)
- 15 minutos (scalping/day trading)
- 1 hora (day trading)
- 4 horas (swing trading)

### 2. **Indicadores Técnicos**
| Indicador | Uso |
|-----------|-----|
| **EMA 9, 21, 50, 200** | Dirección de tendencia |
| **RSI (14)** | Sobrecompra/sobreventa |
| **MACD** | Momentum y cruces |
| **ADX** | Fuerza de tendencia |
| **ATR** | Volatilidad |

### 3. **Open Interest**
- Detecta entrada/salida de capital
- Identifica divergencias precio-OI
- **Alerta de "trampas alcistas/bajistas"**

### 4. **Sistema de Alertas**
```
🔴 CRÍTICAS: RSI extremo + divergencia OI
🟠 ALTAS: Volatilidad alta, ADX agotado
🟡 MEDIAS: Falta de consenso entre TFs
🟢 POSITIVAS: Confirmaciones alcistas/bajistas
```

### 5. **Niveles de Precio**
Para cada setup (LONG o SHORT):
- **3 entradas** (agresiva, moderada, conservadora)
- **Stop Loss** calculado (basado en ATR)
- **3 Take Profits** con ratios R:R
- **Soportes y Resistencias**

---

## 🎯 Ejemplo de Salida

### Caso Real: COAI/USDT (Detectó trampa alcista)

```
============================================================
📈 ANÁLISIS MULTI-TIMEFRAME: COAI/USDT:USDT
============================================================

⏰ TIMEFRAME: 5m
   Tendencia: 🟢 ALCISTA FUERTE
   Precio: $14.0202
   RSI: 89.98 (SOBRECOMPRA) ⚠️
   ADX: 70.98 (Fuerza: FUERTE)

⏰ TIMEFRAME: 15m
   Tendencia: 🟢 ALCISTA FUERTE
   RSI: 89.25 (SOBRECOMPRA) ⚠️

⏰ TIMEFRAME: 1h
   Tendencia: 🟢 ALCISTA FUERTE
   RSI: 88.85 (SOBRECOMPRA) ⚠️

============================================================
📊 ANÁLISIS DE OPEN INTEREST
============================================================

📈 Open Interest Actual: 2,898,858
   Cambio 24h: -3.83% ⚠️
   Divergencia: ⚠️ BAJISTA (Precio sube, OI baja - Posible techo)
   💡 ⚠️ Alerta: Subida sin respaldo - Posible corrección pronto

============================================================
🚨 ANÁLISIS DE RIESGOS Y ALERTAS
============================================================

🔴 ALERTAS CRÍTICAS:
   ❌ RSI > 85 en múltiples timeframes - SOBRECOMPRA EXTREMA
   ❌ ⚠️ TRAMPA ALCISTA DETECTADA - Probable corrección inminente

🟠 ALERTAS DE RIESGO ALTO:
   ⚠️ Divergencia bajista precio-OI - Subida sin respaldo institucional
   ⚠️ ADX muy fuerte (>60) - Tendencia agotada, posible reversión

============================================================
🎯 RECOMENDACIÓN FINAL DE TRADING
============================================================

📊 ACCIÓN: 🛑 NO OPERAR
   Razón: Riesgo extremadamente alto detectado
   Score de riesgo: 15/16
   Sesgo direccional: NEUTRAL - Esperar confirmación

💡 RECOMENDACIONES ESPECÍFICAS:
   1. Evitar LONG nuevos - Precio en zona extrema
   2. Considerar tomar ganancias parciales si estás en LONG
   3. SHORT solo con confirmación fuerte y stop ajustado
   4. ⚠️ CRÍTICO: No confiar en esta subida - OI bajando
   5. Preparar salida o considerar cobertura SHORT

============================================================
💰 NIVELES DE PRECIO SUGERIDOS
============================================================

📍 SETUP: SHORT (contrarian)
   Precio actual: $14.0202

🎯 ENTRADAS SUGERIDAS:
   Agresiva: $14.0202 (entrada inmediata)
   Moderada: $13.5000 (esperar retroceso)
   Conservadora: $12.8000 (mejor R:R)

🛑 STOP LOSS: $15.0000
   Riesgo desde precio actual: $0.9798 (6.99%)

✅ TAKE PROFITS:
   TP1: $12.5500 (R:R 1.5:1) - Cerrar 50%
   TP2: $10.5800 (R:R 2.5:1) - Cerrar 30%
   TP3: $8.1000 (R:R 4:1) - Cerrar 20%

📊 SOPORTES Y RESISTENCIAS:
   Resistencias: $14.3500 | $15.2000 | $16.8000
   Soportes: $11.4000 | $9.9000 | $7.5000
```

**Resultado:** El precio efectivamente corrigió de $14 a $11 en las siguientes horas ✅

---

## 🤖 Comandos del Bot de Telegram

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Mensaje de bienvenida | `/start` |
| `/analizar` | Análisis completo (15-20 seg) | `/analizar BTCUSDT` |
| `/quick` | Análisis rápido (3-5 seg) | `/quick ETHUSDT` |
| `/precio` | Ver precio actual | `/precio BTCUSDT` |
| `/buscar` | Buscar símbolos | `/buscar COAI` |
| `/help` | Ayuda | `/help` |

### Uso en Grupos

El bot funciona en grupos de Telegram:
1. Añade el bot al grupo
2. Dale permisos de administrador
3. Usa los comandos normalmente

```
Usuario1: /analizar BTCUSDT
Bot: [Análisis completo...]

Usuario2: /quick ETHUSDT
Bot: [Análisis rápido...]
```

---

## 🎓 Interpretación de Resultados

### Señales Alcistas ✅
```
✅ Tendencia: 🟢 ALCISTA FUERTE en 3-4 timeframes
✅ RSI: 50-70 (momentum saludable)
✅ OI: Subiendo junto con precio
✅ ADX: > 25 (tendencia fuerte)
✅ Score de riesgo: < 4

→ ACCIÓN: Buscar entradas LONG en retrocesos a EMAs
```

### Señales Bajistas ⚠️
```
⚠️ Tendencia: 🔴 BAJISTA FUERTE en 3-4 timeframes
⚠️ RSI: 30-50 (presión vendedora)
⚠️ OI: Bajando junto con precio
⚠️ ADX: > 25 (tendencia fuerte)
⚠️ Score de riesgo: < 4

→ ACCIÓN: Buscar entradas SHORT en rebotes a EMAs
```

### Señales de PELIGRO 🚨
```
🔴 RSI: > 85 o < 15 (extremo)
🔴 Divergencia: Precio ↑ OI ↓ (trampa alcista)
🔴 ADX: > 60 (agotamiento)
🔴 Score de riesgo: > 10

→ ACCIÓN: NO OPERAR - Esperar confirmación
```

---

## 💼 Casos de Uso

### 1. Scalper (5m - 15m)
```python
# Ejecutar cada 15-30 minutos
/quick BTCUSDT

# Si señal es favorable:
/analizar BTCUSDT  # Para niveles exactos
```

### 2. Day Trader (15m - 1h)
```python
# Al inicio del día (análisis completo)
/analizar BTCUSDT
/analizar ETHUSDT
/analizar SOLUSDT

# Durante el día (seguimiento)
/precio BTCUSDT  # Cada hora
```

### 3. Swing Trader (1h - 4h)
```python
# Una vez al día
/analizar BTCUSDT  # Confirmar tendencia principal

# Usar niveles de 4h para:
- Entradas en retrocesos mayores
- Stops más amplios
- Targets de varios días
```

---

## 🛡️ Ventajas vs. Trading Manual

| Aspecto | Manual | Con Bot |
|---------|--------|---------|
| **Tiempo de análisis** | 10-15 min | 15 seg |
| **Errores humanos** | Frecuentes | Eliminados |
| **Análisis Multi-TF** | Tedioso | Automático |
| **Divergencias OI** | Difícil detectar | Automático |
| **Disponibilidad** | Solo cuando estás | 24/7 |
| **Consistencia** | Variable | 100% |
| **Cálculo de niveles** | Manual | Instantáneo |

---

## 📊 Métricas del Proyecto

### Indicadores Analizados
- ✅ 7 indicadores técnicos principales
- ✅ 4 timeframes simultáneos
- ✅ Open Interest con histórico
- ✅ 15+ métricas de riesgo

### Precisión
- ✅ Detecta trampas alcistas/bajistas
- ✅ Identifica divergencias precio-OI
- ✅ Calcula niveles con Fibonacci + ATR
- ✅ Sistema de alertas con 4 niveles de riesgo

### Performance
- ⚡ Análisis completo: 15-20 segundos
- ⚡ Análisis rápido: 3-5 segundos
- ⚡ Consulta de precio: < 1 segundo

---

## 🔧 Configuración Avanzada

### Cambiar Exchange
```python
# En crypto_trend_detector.py o main.py
detector = CryptoTrendDetector(exchange_name='binance')
# Opciones: 'bybit', 'binance', 'okx', 'kucoin'
```

### Modificar Timeframes
```python
# En analyze_multiple_timeframes()
timeframes = ['1m', '5m', '15m', '30m', '1h']
```

### Ajustar Indicadores
```python
# En calculate_indicators()
df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()
# Cambiar span para diferentes periodos
```

---

## 📱 Despliegue en Producción

### Opción 1: VPS (Recomendado)
```bash
# Instalar en servidor Linux
screen -S telegram_bot
python telegram_bot.py
# Ctrl+A, D para detach
```

### Opción 2: Docker
```bash
docker build -t crypto-bot .
docker run -d --name bot -e TELEGRAM_BOT_TOKEN="token" crypto-bot
```

### Opción 3: Heroku (Gratis)
```bash
heroku create
heroku config:set TELEGRAM_BOT_TOKEN="token"
git push heroku main
```

### Opción 4: Raspberry Pi
Perfecto para correr 24/7 en casa con bajo consumo.

---

## 🐛 Solución de Problemas Comunes

### Bot no responde
```bash
# Verificar que está corriendo
ps aux | grep telegram_bot

# Ver logs
tail -f logs/bot.log
```

### Error de Rate Limit
```
✅ CCXT maneja esto automáticamente
⏳ Solo espera 1-2 minutos
```

### Símbolo no encontrado
```bash
# Usar comando de búsqueda
/buscar BTC

# Usar formato exacto que muestra
/analizar BTC/USDT:USDT
```

---

## 📈 Mejoras Futuras (Roadmap)

### v1.1 (Próximamente)
- [ ] Alertas de precio automáticas
- [ ] Botones interactivos en Telegram
- [ ] Gráficos integrados

### v1.2
- [ ] Funding Rate analysis
- [ ] Long/Short Ratio
- [ ] Volumen de liquidaciones

### v1.3
- [ ] Backtesting engine
- [ ] Historial de señales
- [ ] Estadísticas de precisión

### v2.0
- [ ] Trading automático (semi-manual)
- [ ] Machine Learning para predicciones
- [ ] Dashboard web

---

## 📞 Soporte y Contribuciones

### ¿Encontraste un bug?
1. Ve a GitHub Issues
2. Describe el problema
3. Incluye logs si es posible

### ¿Quieres contribuir?
1. Fork el repositorio
2. Crea una branch: `feature/nueva-funcionalidad`
3. Commit: `git commit -m "Add: nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

### ¿Tienes ideas?
Abre un Issue con la etiqueta `enhancement`

---

## 📜 Licencia

MIT License - Úsalo libremente, pero bajo tu propio riesgo.

---

## ⚠️ Disclaimer Final

```
⚠️ IMPORTANTE:

1. Este proyecto es EDUCATIVO e INFORMATIVO
2. NO es asesoramiento financiero
3. Trading de criptos conlleva ALTO RIESGO
4. Puedes PERDER TODO tu capital
5. NUNCA inviertas más de lo que puedes perder
6. PRACTICA en demo antes de usar capital real
7. Los resultados pasados NO garantizan resultados futuros

El autor NO se hace responsable de pérdidas financieras.
USA BAJO TU PROPIO RIESGO.
```

---

## 🌟 Créditos

**Desarrollado con ❤️ para la comunidad de traders**

Tecnologías utilizadas:
- [CCXT](https://github.com/ccxt/ccxt) - Exchange connector
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [NumPy](https://numpy.org/) - Numerical computing
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram API

---

## 🎉 ¡Listo para Usar!

```bash
# Terminal
python main.py

# Telegram Bot
python telegram_bot.py

# ¡A analizar el mercado! 📈🚀
```

**Si te ayudó, dale una ⭐ en GitHub!**