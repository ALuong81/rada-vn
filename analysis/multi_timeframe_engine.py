def analyze_trend(stock):

    price = stock.get("price", 0)
    resistance = stock.get("resistance", 0)

    if resistance == 0:
        stock["trend"] = "TRUNG TÍNH"
        return stock

    ratio = price / resistance

    if ratio > 0.9:
        stock["trend"] = "ĐỒNG THUẬN MẠNH"

    elif ratio > 0.75:
        stock["trend"] = "ĐỒNG THUẬN"

    else:
        stock["trend"] = "YẾU"

    return stock


def scan_trend(stocks):

    for s in stocks:
        analyze_trend(s)

    return stocks
