from crypto_trend_detector import CryptoTrendDetector


if __name__ == "__main__":
    print("🚀 INICIANDO DETECTOR DE TENDENCIAS CRYPTO\n")
    
    # Inicializar detector (puedes cambiar a 'binance', 'okx', etc.)
    detector = CryptoTrendDetector(exchange_name='bybit')
    
    # Preguntar al usuario qué símbolo analizar
    symbol_input = input("\n¿Qué moneda quieres analizar? (ejemplo: BTC/USDT o BTCUSDT): ").strip()
    
    if not symbol_input:
        symbol_input = 'BTC/USDT'
        print(f"⚠️  Usando símbolo por defecto: {symbol_input}")
    
    # Buscar el símbolo correcto
    symbol = detector.normalize_symbol(symbol_input)
    
    if symbol is None:
        print(f"\n❌ No se encontró el símbolo '{symbol_input}'")
        print("💡 Buscando símbolos similares...\n")
        
        # Extraer el ticker base (BTC, ETH, etc.)
        base_search = symbol_input.split('/')[0] if '/' in symbol_input else symbol_input.replace('USDT', '').replace('USD', '')
        matches = detector.search_symbol(base_search)
        
        if matches:
            print("📋 Símbolos disponibles:")
            for i, match in enumerate(matches, 1):
                print(f"   {i}. {match}")
            print("\n💡 Usa uno de estos símbolos exactos\n")
        else:
            print(f"⚠️  No se encontraron símbolos similares a '{base_search}'")
        exit(1)
    
    print(f"\n✅ Símbolo encontrado: {symbol}\n")
    
    try:
        # Análisis completo multi-timeframe
        results = detector.analyze_multiple_timeframes(symbol)
        
        if not results:
            print("\n❌ No se pudo realizar el análisis")
            exit(1)
        
        # Análisis detallado de 15 minutos
        print(f"\n{'='*60}")
        print("📊 ANÁLISIS DETALLADO DE 15 MINUTOS")
        print(f"{'='*60}\n")
        
        df = detector.get_ohlcv_data(symbol, '15m', limit=200)
        if df is not None:
            df = detector.calculate_indicators(df)
            trend = detector.identify_trend(df)
            
            # Mostrar últimas 5 velas
            print("📈 Últimas 5 velas:")
            print(df[['open', 'high', 'low', 'close', 'volume']].tail())
            print()
            
            # Mostrar indicadores actuales
            print("🔍 Indicadores actuales:")
            last_row = df.iloc[-1]
            print(f"   EMA 9: ${last_row['ema_9']:.4f}")
            print(f"   EMA 21: ${last_row['ema_21']:.4f}")
            print(f"   EMA 50: ${last_row['ema_50']:.4f}")
            print(f"   RSI: {last_row['rsi']:.2f}")
            print(f"   MACD: {last_row['macd']:.4f}")
            print(f"   ADX: {last_row['adx']:.2f}")
        
    except Exception as e:
        print(f"❌ Error en el análisis: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Asegúrate de tener instalado: pip install ccxt pandas numpy")