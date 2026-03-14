def ai_breakout_predict(stock):

    rs = stock.get("rs_rating",0)
    volume = stock.get("volume",0)
    avg_volume = stock.get("avg_volume",0)
    pattern = stock.get("pattern","")
    vcp = stock.get("vcp","")

    if avg_volume == 0:
        return 0

    vol_ratio = volume / avg_volume

    score = 0

    if rs > 85:
        score += 30

    if vol_ratio > 1.5:
        score += 25

    if pattern == "BREAKOUT PATTERN":
        score += 25

    if vcp == "CÓ":
        score += 20

    return score
