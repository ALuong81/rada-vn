def market_breadth(stocks):

    total = 0
    up = 0
    down = 0

    for s in stocks:

        if not isinstance(s, dict):
            continue

        change = s.get("change")

        if change is None:
            continue

        total += 1

        if change > 0:
            up += 1
        elif change < 0:
            down += 1

    if total == 0:
        return {
            "market_status": "UNKNOWN",
            "market_regime": "UNKNOWN",
            "breadth": "UNKNOWN",
            "adv_ratio": 0
        }

    ratio = up / total

    # MARKET REGIME
    if ratio >= 0.65:
        status = "RISK ON"
        regime = "UPTREND"

    elif ratio >= 0.55:
        status = "TÍCH CỰC"
        regime = "UPTREND NHẸ"

    elif ratio >= 0.45:
        status = "TRUNG LẬP"
        regime = "SIDEWAYS"

    else:
        status = "RISK OFF"
        regime = "DOWNTREND"

    # MARKET BREADTH
    if ratio >= 0.65:
        breadth = "THỊ TRƯỜNG RỘNG"
    elif ratio >= 0.50:
        breadth = "TRUNG BÌNH"
    else:
        breadth = "THỊ TRƯỜNG HẸP"

    return {
        "market_status": status,
        "market_regime": regime,
        "breadth": breadth,
        "adv_ratio": round(ratio * 100, 1)
    }
