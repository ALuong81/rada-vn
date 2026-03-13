def detect_volume_signal(stock):

    vol = stock.get("volume", 0)
    avg = stock.get("avg_volume", 0)

    if avg == 0:
        stock["money_signal"] = "BÌNH THƯỜNG"
        return stock

    ratio = vol / avg

    if ratio > 2:
        stock["money_signal"] = "DÒNG TIỀN TỔ CHỨC"

    elif ratio > 1.5:
        stock["money_signal"] = "MẠNH"

    else:
        stock["money_signal"] = "BÌNH THƯỜNG"

    return stock


def scan_volume(stocks):

    for s in stocks:
        detect_volume_signal(s)

    return stocks
