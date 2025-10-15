# 🤖 Configuración del Bot de Telegram

Guía completa para configurar y ejecutar el bot de análisis de criptomonedas en Telegram.

---

## 📋 Requisitos Previos

1. Python 3.8+
2. Cuenta de Telegram
3. Token del bot (lo obtendremos en el paso siguiente)

---

## 🔧 Paso 1: Crear el Bot en Telegram

### 1.1 Hablar con BotFather

1. Abre Telegram y busca: **@BotFather**
2. Inicia conversación con `/start`
3. Crea un nuevo bot con: `/newbot`

### 1.2 Configurar el Bot

BotFather te preguntará:

```
Alright, a new bot. How are we going to call it? 
Please choose a name for your bot.
```

**Ejemplo de respuesta:** `Crypto Trend Analyzer`

```
Good. Now let's choose a username for your bot. 
It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
```

**Ejemplo de respuesta:** `crypto_trend_analyzer_bot`

### 1.3 Obtener el Token

BotFather te dará un token como este:

```
Done! Congratulations on your new bot. You will find it at t.me/crypto_trend_analyzer_bot. 
You can now add a description...

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

**⚠️ IMPORTANTE:** Guarda ese token de forma segura, lo necesitarás.

---

## 📦 Paso 2: Instalar Dependencias

### 2.1 Actualizar requirements.txt

Añade la librería de Telegram al archivo `requirements.txt`:

```bash
# Crypto Trend Detector - Dependencias
ccxt>=4.0.0
pandas>=2.0.0
numpy>=1.24.0

# Bot de Telegram
python-telegram-bot>=20.0
```

### 2.2 Instalar

```bash
# Activar entorno virtual
# Windows
myenv\Scripts\activate

# Linux/Mac
source myenv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# O instalar solo Telegram bot
pip install python-telegram-bot
```

---

## 🔐 Paso 3: Configurar el Token

### Opción 1: Variable de Entorno (Recomendado)

#### Windows (PowerShell):
```powershell
# Temporal (solo para la sesión actual)
$env:TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890"

# Permanente (agregar al perfil)
[System.Environment]::SetEnvironmentVariable("TELEGRAM_BOT_TOKEN", "TU_TOKEN_AQUI", "User")
```

#### Windows (CMD):
```cmd
set TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

#### Linux/Mac:
```bash
# Temporal
export TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890"

# Permanente (añadir al ~/.bashrc o ~/.zshrc)
echo 'export TELEGRAM_BOT_TOKEN="TU_TOKEN_AQUI"' >> ~/.bashrc
source ~/.bashrc
```

### Opción 2: Archivo .env (Alternativa)

Crea un archivo `.env` en la raíz del proyecto:

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

Instala python-dotenv:
```bash
pip install python-dotenv
```

Modifica `telegram_bot.py` para cargar el .env:
```python
from dotenv import load_dotenv
load_dotenv()  # Añadir al inicio del archivo
```

---

## 🚀 Paso 4: Ejecutar el Bot

### 4.1 Iniciar el Bot

```bash
# Asegúrate de estar en el entorno virtual
python telegram_bot.py
```

Deberías ver:
```
🤖 Bot de Telegram iniciado correctamente
✅ Esperando comandos...
💡 Presiona Ctrl+C para detener el bot

📋 Comandos disponibles:
   /analizar BTCUSDT
   /quick ETHUSDT
   /precio BTCUSDT
   /buscar BTC
```

### 4.2 Probar el Bot

1. Abre Telegram
2. Busca tu bot: `@crypto_trend_analyzer_bot` (o el nombre que elegiste)
3. Inicia conversación: `/start`
4. Prueba un análisis: `/analizar BTCUSDT`

---

## 👥 Paso 5: Añadir el Bot a un Grupo

### 5.1 Habilitar Modo Grupo en BotFather

1. Habla con @BotFather
2. Envía: `/mybots`
3. Selecciona tu bot
4. Click en "Bot Settings"
5. Click en "Group Privacy"
6. Click en "Turn off" (desactivar privacidad de grupo)

### 5.2 Añadir Bot al Grupo

1. Abre el grupo en Telegram
2. Click en nombre del grupo → "Add members"
3. Busca tu bot y añádelo
4. Dale permisos de administrador (opcional, pero recomendado)

### 5.3 Usar en el Grupo

En el grupo, los comandos funcionan igual:
```
/analizar BTCUSDT
/quick ETHUSDT
/precio BTCUSDT
```

---

## 📱 Comandos Disponibles

### Análisis Completo
```
/analizar BTCUSDT
```
- Análisis multi-timeframe (5m, 15m, 1h, 4h)
- Open Interest
- Alertas de riesgo
- Niveles de precio sugeridos
- Recomendación final

### Análisis Rápido
```
/quick ETHUSDT
```
- Solo timeframe de 15m
- Respuesta inmediata
- Ideal para consultas rápidas

### Ver Precio
```
/precio BTCUSDT
```
- Precio actual
- Cambio en últimos 5 minutos

### Buscar Símbolos
```
/buscar BTC
```
- Encuentra todos los pares con BTC
- Útil para descubrir símbolos disponibles

### Información
```
/help - Ayuda general
/exchanges - Lista de exchanges soportados
/start - Mensaje de bienvenida
```

---

## 🔥 Ejemplos de Uso Real

### Ejemplo 1: Trading Matutino
```
Usuario: /analizar BTCUSDT

Bot: 📊 ANÁLISIS COMPLETO: BTC/USDT:USDT

📈 Multi-Timeframe:
• 5m: 🟢 ALCISTA
• 15m: 🟢 ALCISTA FUERTE
• 1h: 🟢 ALCISTA FUERTE
• 4h: 🟢 ALCISTA

💰 Precio: $42,150.50

📊 Open Interest:
• Actual: 125,450,000
• Cambio 24h: +8.45%
• ✅ Alto interés del mercado - Momentum positivo

🎯 RECOMENDACIÓN:
✅ CONDICIONES FAVORABLES
Score de riesgo: 3/16
Sesgo: LONG - Buscar entradas en soporte

💰 NIVELES (LONG):
• Entrada: $41,850.00
• Stop Loss: $41,200.00
• TP1: $42,800.00 (R:R 1.5:1)
• TP2: $43,500.00 (R:R 2.5:1)

✅ Análisis completado
```

### Ejemplo 2: Consulta Rápida
```
Usuario: /quick ETHUSDT

Bot: 📊 Análisis Rápido: ETH/USDT:USDT

💰 Precio: $2,245.80
📈 Tendencia (15m): 🔴 BAJISTA

Indicadores:
• RSI: 35.20 (BAJISTA)
• MACD: BAJISTA
• ADX: 28.50 (Fuerza: FUERTE)
• EMAs: 1/5

Open Interest:
• OI: 45,230,000 (-2.50%)
• 📉 Cierre de posiciones long - Presión vendedora fuerte

💡 Usa /analizar para análisis completo
```

---

## 🛡️ Seguridad

### ✅ Buenas Prácticas

1. **Nunca compartas tu token** del bot públicamente
2. **Usa variables de entorno**, no hardcodees el token en el código
3. **Añade .env al .gitignore** si usas archivos de configuración
4. **Limita acceso** del bot solo a grupos de confianza
5. **Monitorea logs** para detectar uso inusual

### ⚠️ Si tu Token se Compromete

1. Habla con @BotFather
2. Envía: `/mybots`
3. Selecciona tu bot
4. Click en "API Token"
5. Click en "Revoke current token"
6. Actualiza tu código con el nuevo token

---

## 🔧 Ejecución en Producción

### Opción 1: Ejecutar en Servidor (Linux)

```bash
# Instalar screen para mantener proceso activo
sudo apt install screen

# Crear sesión
screen -S telegram_bot

# Activar entorno y ejecutar
source myenv/bin/activate
python telegram_bot.py

# Detach con: Ctrl+A, luego D
# Reattach con: screen -r telegram_bot
```

### Opción 2: Systemd Service (Linux)

Crear archivo `/etc/systemd/system/telegram-crypto-bot.service`:

```ini
[Unit]
Description=Telegram Crypto Analysis Bot
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/tu/proyecto
Environment="TELEGRAM_BOT_TOKEN=tu_token_aqui"
ExecStart=/ruta/a/tu/proyecto/myenv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-crypto-bot
sudo systemctl start telegram-crypto-bot
sudo systemctl status telegram-crypto-bot
```

### Opción 3: Docker (Recomendado para Producción)

Crear `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TELEGRAM_BOT_TOKEN=""

CMD ["python", "telegram_bot.py"]
```

Ejecutar:
```bash
docker build -t crypto-telegram-bot .
docker run -d --name crypto-bot -e TELEGRAM_BOT_TOKEN="tu_token" crypto-telegram-bot
```

### Opción 4: Heroku (Gratis)

1. Crear cuenta en Heroku
2. Crear `Procfile`:
```
worker: python telegram_bot.py
```
3. Subir a Heroku:
```bash
heroku create crypto-trend-bot
heroku config:set TELEGRAM_BOT_TOKEN="tu_token"
git push heroku main
heroku ps:scale worker=1
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Linux/Mac con screen
screen -r telegram_bot

# Docker
docker logs -f crypto-bot

# Systemd
sudo journalctl -u telegram-crypto-bot -f
```

### Logs Importantes

El bot registra:
- ✅ Comandos ejecutados
- ⚠️ Errores de análisis
- 🔍 Símbolos buscados
- 📊 Análisis completados

---

## 🐛 Troubleshooting

### Problema: "No se encontró TELEGRAM_BOT_TOKEN"

**Solución:**
```bash
# Verificar que la variable está configurada
echo $TELEGRAM_BOT_TOKEN  # Linux/Mac
echo %TELEGRAM_BOT_TOKEN%  # Windows CMD
$env:TELEGRAM_BOT_TOKEN    # Windows PowerShell
```

### Problema: "Conflict: terminated by other getUpdates request"

**Causa:** El bot está corriendo en dos lugares al mismo tiempo

**Solución:** Detén todas las instancias del bot y ejecuta solo una

### Problema: Bot no responde en grupo

**Solución:** 
1. Verifica que desactivaste "Group Privacy" en BotFather
2. Reinicia el bot
3. Escribe comandos con `/` al inicio

### Problema: "Rate limit exceeded"

**Causa:** Demasiadas peticiones al exchange

**Solución:** El bot tiene rate limiting automático, espera 1-2 minutos

---

## 📈 Mejoras Futuras

### Funcionalidades Planeadas

- [ ] Alertas automáticas cuando el precio alcance cierto nivel
- [ ] Seguimiento de múltiples símbolos simultáneamente
- [ ] Gráficos integrados en Telegram
- [ ] Botones interactivos para navegación
- [ ] Historial de análisis
- [ ] Recordatorios personalizables
- [ ] Integración con TradingView

---

## 💡 Tips de Uso

### 1. Atajos de Teclado en Telegram
- `Ctrl + K`: Buscar conversaciones
- `Ctrl + F`: Buscar en chat actual
- `/`: Mostrar comandos disponibles

### 2. Uso en Trading Real
```
# Rutina matutina
/analizar BTCUSDT
/analizar ETHUSDT
/quick SOLUSDT

# Durante el día
/precio BTCUSDT  # Cada 15-30 min

# Setup de trading
/analizar [TU_SÍMBOLO]  # Antes de entrar
```

### 3. Uso en Grupos
- Menciona al bot: `@tu_bot /analizar BTCUSDT`
- O simplemente: `/analizar BTCUSDT`

---

## 📞 Soporte

¿Problemas o preguntas?

- 🐛 Reportar bugs: GitHub Issues
- 💬 Telegram: @tu_usuario
- 📧 Email: tu-email@ejemplo.com

---

## ⚖️ Disclaimer

Este bot es para fines educativos e informativos. No es asesoramiento financiero. Usa bajo tu propio riesgo.

---

**¡Bot listo para analizar el mercado 24/7!** 📈🤖