def supply_dryup(stock):

    vol = stock.get("volume",0)
    avg = stock.get("avg_volume",0)

    if avg == 0:
        return "BÌNH THƯỜNG"

    ratio = vol / avg

    if ratio < 0.6:
        return "CUNG CẠN"

    if ratio < 0.8:
        return "SIẾT CUNG"

    return "BÌNH THƯỜNG"
