def detect_smart_money(stock):

    volume = stock.get("volume", 0)
    avg_volume = stock.get("avg_volume", 0)
    change = stock.get("change", 0)

    if avg_volume == 0:
        stock["smart_money"] = "KHÔNG"
        return stock

    if volume > avg_volume * 2 and change > 1:
        stock["smart_money"] = "MẠNH"

    elif volume > avg_volume * 1.5:
        stock["smart_money"] = "CÓ"

    else:
        stock["smart_money"] = "KHÔNG"

    return stock


def scan_smart_money(stocks):

    results = []

    for s in stocks:

        if not isinstance(s, dict):
            continue

        s = detect_smart_money(s)

        results.append(s)

    return results
