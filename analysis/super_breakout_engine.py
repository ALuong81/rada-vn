def super_breakout(stock):

    rs = stock.get("rs_score",0)
    volume = stock.get("volume",0)
    avg_volume = stock.get("avg_volume",1)
    meta = stock.get("meta_score",0)

    score = 0

    if rs > 80:
        score += 1

    if volume > avg_volume*1.5:
        score += 1

    if meta > 80:
        score += 1

    if score >= 3:
        return "SIÊU BREAKOUT"

    if score == 2:
        return "CÓ KHẢ NĂNG"

    return "THẤP"

def detect_super_breakout(stock):

    df = stock.get("data")

    if df is None or len(df) < 60:
        return "THẤP"

    close = df["close"]
    volume = df["volume"]

    highest = close.tail(50).max()
    price = close.iloc[-1]

    avg_vol = volume.tail(20).mean()
    today_vol = volume.iloc[-1]

    # breakout mạnh
    if price >= highest * 0.98 and today_vol > avg_vol * 1.5:
        return "CAO"

    # chuẩn bị breakout
    if price >= highest * 0.95:
        return "TRUNG BÌNH"

    return "THẤP"
