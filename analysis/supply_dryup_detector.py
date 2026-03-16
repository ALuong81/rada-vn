def supply_dryup(stock):

    volume = stock.get("volume", 0)
    avg_volume = stock.get("avg_volume", 0)

    if avg_volume == 0:
        return "UNKNOWN"

    ratio = volume / avg_volume

    if ratio < 0.6:
        return "CUNG CẠN"

    if ratio < 0.8:
        return "SIẾT CUNG"

    return "BÌNH THƯỜNG"
