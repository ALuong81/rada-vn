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
