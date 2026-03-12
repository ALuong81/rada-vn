def supply_dryup(stock):

    ratio = stock["volume"] / stock["avg_volume"]

    if ratio < 0.6:

        return "CUNG CẠN"

    if ratio < 0.8:

        return "SIẾT CUNG"

    return "BÌNH THƯỜNG"
