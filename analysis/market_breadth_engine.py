def market_breadth(stocks):

    total = len(stocks)

    if total == 0:
        return {
            "market_status": "UNKNOWN",
            "market_regime": "SIDEWAYS",
            "breadth": "UNKNOWN",
            "adv_ratio": 0
        }

    up = 0

    for s in stocks:
        if s.get("change", 0) > 0:
            up += 1

    ratio = up / total

    if ratio > 0.65:
        status = "RISK ON"
        regime = "UPTREND MẠNH"
        breadth = "THỊ TRƯỜNG RỘNG"

    elif ratio > 0.55:
        status = "RISK ON"
        regime = "UPTREND"
        breadth = "KHÁ RỘNG"

    elif ratio > 0.45:
        status = "TRUNG LẬP"
        regime = "SIDEWAYS"
        breadth = "TRUNG BÌNH"

    else:
        status = "RISK OFF"
        regime = "DOWNTREND"
        breadth = "THỊ TRƯỜNG HẸP"

    return {
        "market_status": status,
        "market_regime": regime,
        "breadth": breadth,
        "adv_ratio": round(ratio * 100, 1)
    }
