"""
Bot de Telegram para Análisis de Criptomonedas
Permite consultar tendencias y análisis técnico desde Telegram
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from crypto_trend_detector import CryptoTrendDetector
import io

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializar detector global
detector = CryptoTrendDetector(exchange_name='bybit')

# ============================================================================
# COMANDOS DEL BOT
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Mensaje de bienvenida"""
    welcome_message = """
🤖 **Bot de Análisis Crypto - ACTIVO**

Comandos disponibles:

📊 **Análisis:**
/analizar BTCUSDT - Análisis completo multi-timeframe
/quick ETHUSDT - Análisis rápido (solo consenso)
/precio BTCUSDT - Ver precio actual

🔍 **Búsqueda:**
/buscar BTC - Buscar símbolos disponibles

ℹ️ **Información:**
/help - Ver esta ayuda
/exchanges - Ver exchanges soportados

💡 **Ejemplos:**
`/analizar BTCUSDT`
`/analizar BTC/USDT`
`/quick ETHUSDT`
`/buscar COAI`

⚡ El bot está optimizado para scalping y day trading.
Desarrollado con ❤️ para traders.
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    await start(update, context)

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /analizar SYMBOL - Análisis completo
    Ejemplo: /analizar BTCUSDT
    """
    if not context.args:
        await update.message.reply_text(
            "❌ Uso incorrecto\n\n"
            "✅ Uso correcto:\n"
            "/analizar BTCUSDT\n"
            "/analizar BTC/USDT\n"
            "/analizar ETHUSDT"
        )
        return
    
    symbol_input = context.args[0].upper()
    
    # Mensaje de espera
    wait_msg = await update.message.reply_text(
        f"🔄 Analizando {symbol_input}...\n"
        "⏳ Esto puede tomar 10-15 segundos..."
    )
    
    try:
        # Normalizar símbolo
        symbol = detector.normalize_symbol(symbol_input)
        
        if symbol is None:
            # Buscar símbolos similares
            base_search = symbol_input.replace('USDT', '').replace('USD', '')
            matches = detector.search_symbol(base_search)
            
            error_msg = f"❌ Símbolo '{symbol_input}' no encontrado\n\n"
            if matches:
                error_msg += "💡 ¿Quisiste decir?\n"
                for match in matches[:5]:
                    error_msg += f"   • {match}\n"
                error_msg += "\n💡 Usa: /analizar SÍMBOLO_EXACTO"
            else:
                error_msg += "💡 No se encontraron símbolos similares"
            
            await wait_msg.edit_text(error_msg)
            return
        
        # Realizar análisis completo
        result_text = await perform_full_analysis(symbol, detector)
        
        # Telegram tiene límite de 4096 caracteres
        if len(result_text) > 4096:
            # Dividir en múltiples mensajes
            parts = [result_text[i:i+4000] for i in range(0, len(result_text), 4000)]
            await wait_msg.delete()
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await wait_msg.edit_text(result_text, parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"Error en analyze: {e}")
        await wait_msg.edit_text(
            f"❌ Error al analizar {symbol_input}\n\n"
            f"Detalles: {str(e)}\n\n"
            "💡 Intenta de nuevo o usa /help"
        )

async def quick_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /quick SYMBOL - Análisis rápido
    Ejemplo: /quick BTCUSDT
    """
    if not context.args:
        await update.message.reply_text(
            "❌ Uso incorrecto\n\n"
            "✅ Uso correcto: /quick BTCUSDT"
        )
        return
    
    symbol_input = context.args[0].upper()
    wait_msg = await update.message.reply_text(f"🔄 Analizando {symbol_input}...")
    
    try:
        symbol = detector.normalize_symbol(symbol_input)
        if symbol is None:
            await wait_msg.edit_text(f"❌ Símbolo '{symbol_input}' no encontrado")
            return
        
        # Análisis rápido solo del timeframe de 15m
        df = detector.get_ohlcv_data(symbol, '15m', limit=200)
        if df is None or len(df) < 50:
            await wait_msg.edit_text(f"❌ No hay datos suficientes para {symbol}")
            return
        
        df = detector.calculate_indicators(df)
        trend_info = detector.identify_trend(df)
        
        if trend_info is None:
            await wait_msg.edit_text(f"❌ No se pudo analizar {symbol}")
            return
        
        # Open Interest rápido
        oi_analysis = detector.analyze_open_interest(symbol, df)
        
        # Formatear respuesta rápida
        quick_result = f"""
📊 **Análisis Rápido: {symbol}**

💰 **Precio:** ${trend_info['precio_actual']:.4f}
📈 **Tendencia (15m):** {trend_info['tendencia']}

**Indicadores:**
• RSI: {trend_info['rsi']}
• MACD: {trend_info['macd']}
• ADX: {trend_info['adx']}
• EMAs: {trend_info['ema_score']}

**Open Interest:**
"""
        if oi_analysis:
            quick_result += f"""• OI: {oi_analysis['oi_actual']} ({oi_analysis['oi_cambio_24h']})
• {oi_analysis['interpretacion']}
"""
        else:
            quick_result += "• No disponible\n"
        
        quick_result += "\n💡 Usa /analizar para análisis completo"
        
        await wait_msg.edit_text(quick_result, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error en quick_analysis: {e}")
        await wait_msg.edit_text(f"❌ Error: {str(e)}")

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /precio SYMBOL - Ver precio actual"""
    if not context.args:
        await update.message.reply_text("❌ Uso: /precio BTCUSDT")
        return
    
    symbol_input = context.args[0].upper()
    
    try:
        symbol = detector.normalize_symbol(symbol_input)
        if symbol is None:
            await update.message.reply_text(f"❌ Símbolo '{symbol_input}' no encontrado")
            return
        
        df = detector.get_ohlcv_data(symbol, '5m', limit=5)
        if df is None:
            await update.message.reply_text(f"❌ No se pudo obtener precio de {symbol}")
            return
        
        current_price = df['close'].iloc[-1]
        prev_price = df['close'].iloc[-2]
        change = ((current_price - prev_price) / prev_price) * 100
        
        emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
        
        price_msg = f"""
{emoji} **{symbol}**

💰 Precio: **${current_price:.4f}**
📊 Cambio (5m): {change:+.2f}%
⏰ Actualizado: Ahora

💡 Usa /analizar {symbol_input} para más detalles
        """
        await update.message.reply_text(price_msg, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error en get_price: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def search_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar QUERY - Buscar símbolos"""
    if not context.args:
        await update.message.reply_text("❌ Uso: /buscar BTC")
        return
    
    query = context.args[0].upper()
    
    try:
        matches = detector.search_symbol(query)
        
        if matches:
            result = f"🔍 **Símbolos encontrados para '{query}':**\n\n"
            for match in matches[:10]:
                result += f"• `{match}`\n"
            result += f"\n💡 Total: {len(matches)} símbolos"
            result += "\n\n📊 Usa: /analizar SÍMBOLO"
        else:
            result = f"❌ No se encontraron símbolos con '{query}'"
        
        await update.message.reply_text(result, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error en search_symbol: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def list_exchanges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /exchanges - Listar exchanges soportados"""
    exchanges_msg = """
🏦 **Exchanges Soportados:**

✅ Bybit (actual)
✅ Binance
✅ OKX
✅ KuCoin
✅ Coinbase
✅ Kraken
✅ Bitfinex

💡 Para cambiar exchange, contacta al administrador.
    """
    await update.message.reply_text(exchanges_msg, parse_mode='Markdown')

# ============================================================================
# FUNCIÓN AUXILIAR PARA ANÁLISIS COMPLETO
# ============================================================================

async def perform_full_analysis(symbol, detector):
    """
    Realiza un análisis completo y retorna texto formateado
    
    Args:
        symbol: Símbolo normalizado
        detector: Instancia de CryptoTrendDetector
    
    Returns:
        String con análisis completo formateado para Telegram
    """
    results = {}
    timeframes = ['5m', '15m', '1h', '4h']
    
    # Análisis por timeframe
    for tf in timeframes:
        df = detector.get_ohlcv_data(symbol, tf, limit=200)
        if df is not None and len(df) >= 50:
            df = detector.calculate_indicators(df)
            trend_info = detector.identify_trend(df)
            if trend_info:
                results[tf] = trend_info
    
    if not results:
        return f"❌ No hay datos suficientes para analizar {symbol}"
    
    # Análisis de OI
    df_oi = detector.get_ohlcv_data(symbol, '1h', limit=100)
    oi_analysis = None
    if df_oi is not None:
        oi_analysis = detector.analyze_open_interest(symbol, df_oi)
    
    # Análisis de riesgos
    risk_analysis = detector.analyze_risk_alerts(results, oi_analysis)
    
    # Generar recomendación
    recommendation = None
    if risk_analysis:
        recommendation = detector.generate_trading_recommendation(results, oi_analysis, risk_analysis)
    
    # Niveles de precio
    df_levels = detector.get_ohlcv_data(symbol, '15m', limit=100)
    price_levels = None
    if df_levels is not None and len(df_levels) >= 50:
        df_levels = detector.calculate_indicators(df_levels)
        current_price = df_levels['close'].iloc[-1]
        atr = df_levels['atr'].iloc[-1]
        trend_direction = risk_analysis['consensus'] if risk_analysis else 'neutral'
        price_levels = detector.calculate_price_levels(df_levels, current_price, trend_direction, atr)
    
    # Formatear salida
    output = f"📊 **ANÁLISIS COMPLETO: {symbol}**\n\n"
    
    # Timeframes
    output += "**📈 Multi-Timeframe:**\n"
    for tf, data in results.items():
        output += f"• {tf}: {data['tendencia']}\n"
    output += "\n"
    
    # Precio actual
    if results:
        first_tf = list(results.values())[0]
        output += f"💰 **Precio:** ${first_tf['precio_actual']:.4f}\n\n"
    
    # Open Interest
    if oi_analysis:
        output += "**📊 Open Interest:**\n"
        output += f"• Actual: {oi_analysis['oi_actual']}\n"
        output += f"• Cambio 24h: {oi_analysis['oi_cambio_24h']}\n"
        output += f"• {oi_analysis['interpretacion']}\n\n"
    
    # Alertas de riesgo
    if risk_analysis and risk_analysis['alerts']:
        alerts = risk_analysis['alerts']
        if alerts['critico']:
            output += "🔴 **ALERTAS CRÍTICAS:**\n"
            for alert in alerts['critico'][:2]:  # Máximo 2
                output += f"❌ {alert}\n"
            output += "\n"
        
        if alerts['alto']:
            output += "🟠 **RIESGO ALTO:**\n"
            for alert in alerts['alto'][:2]:
                output += f"⚠️ {alert}\n"
            output += "\n"
    
    # Recomendación
    if recommendation:
        output += "**🎯 RECOMENDACIÓN:**\n"
        output += f"{recommendation['action']}\n"
        output += f"Score de riesgo: {recommendation['risk_score']}/16\n"
        output += f"Sesgo: {recommendation['bias']}\n\n"
    
    # Niveles de precio
    if price_levels and price_levels['tipo'] in ['LONG', 'SHORT']:
        output += f"**💰 NIVELES ({price_levels['tipo']}):**\n"
        output += f"• Entrada: ${price_levels['entradas']['moderada']:.4f}\n"
        output += f"• Stop Loss: ${price_levels['stop_loss']:.4f}\n"
        output += f"• TP1: ${price_levels['take_profits']['tp1']:.4f} (R:R {price_levels['riesgo_recompensa']['tp1']}:1)\n"
        output += f"• TP2: ${price_levels['take_profits']['tp2']:.4f} (R:R {price_levels['riesgo_recompensa']['tp2']}:1)\n\n"
    
    output += "✅ Análisis completado"
    
    return output

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja errores del bot"""
    logger.error(f"Update {update} causó error: {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ Ocurrió un error inesperado\n"
            "💡 Intenta de nuevo o usa /help"
        )

# ============================================================================
# MAIN - INICIAR BOT
# ============================================================================

def main():
    """Función principal para iniciar el bot"""
    
    # Obtener token del bot de variable de entorno
    TOKEN = '8246019704:AAGi8nshsuSJMl5zJWeXH28OvnpDyWDTCGk'#os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ ERROR: No se encontró TELEGRAM_BOT_TOKEN")
        print("💡 Configura la variable de entorno:")
        print("   export TELEGRAM_BOT_TOKEN='tu_token_aqui'")
        print("\n📖 Para obtener un token:")
        print("   1. Habla con @BotFather en Telegram")
        print("   2. Usa /newbot")
        print("   3. Sigue las instrucciones")
        print("   4. Copia el token generado")
        return
    
    # Crear aplicación
    application = Application.builder().token(TOKEN).build()
    
    # Registrar comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analizar", analyze))
    application.add_handler(CommandHandler("quick", quick_analysis))
    application.add_handler(CommandHandler("precio", get_price))
    application.add_handler(CommandHandler("buscar", search_symbol))
    application.add_handler(CommandHandler("exchanges", list_exchanges))
    
    # Registrar error handler
    application.add_error_handler(error_handler)
    
    # Mensaje de inicio
    print("🤖 Bot de Telegram iniciado correctamente")
    print("✅ Esperando comandos...")
    print("💡 Presiona Ctrl+C para detener el bot")
    print("\n📋 Comandos disponibles:")
    print("   /analizar BTCUSDT")
    print("   /quick ETHUSDT")
    print("   /precio BTCUSDT")
    print("   /buscar BTC")
    
    # Iniciar bot (long polling)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()