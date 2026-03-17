def score_stock(s):

    close = s.get("close")
    volume = s.get("volume")

    if close is None or volume is None:
        return 0

    if len(close) < 50:
        return 0

    try:

        score = 0

        # ===== PRICE =====
        last_close = float(close.iloc[-1])
        ma20 = float(close.rolling(20).mean().iloc[-1])
        ma50 = float(close.rolling(50).mean().iloc[-1])

        if last_close > ma20:
            score += 20

        if last_close > ma50:
            score += 20

        # ===== VOLUME =====
        avg_vol = float(volume.tail(20).mean())
        last_vol = float(volume.iloc[-1])

        if last_vol > avg_vol:
            score += 20

        # ===== BREAKOUT =====
        highest_50 = float(close.tail(50).max())

        if last_close >= highest_50:
            score += 30

        # ===== MOMENTUM =====
        change = (last_close - float(close.iloc[-10])) / float(close.iloc[-10])

        if change > 0.05:
            score += 10

        return float(score)

    except Exception as e:
        print(f"[SCORE ERROR] {s.get('symbol')}: {e}")
        return 0
