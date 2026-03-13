def risk_filter(stock):

    price = stock.get("price",0)
    resistance = stock.get("resistance",0)
    volume = stock.get("volume",0)
    avg_volume = stock.get("avg_volume",0)

    risk = "BÌNH THƯỜNG"

    if price > resistance * 1.05:
        risk = "NGUY CƠ FAKE BREAKOUT"

    if volume < avg_volume * 0.7:
        risk = "THANH KHOẢN YẾU"

    stock["risk_warning"] = risk

    return stock


def scan_risk(stocks):

    results = []

    for s in stocks:

        if not isinstance(s,dict):
            continue

        s = risk_filter(s)

        results.append(s)

    return results
