def market_breadth(stocks):

    if not stocks:
        return {
            "market_status":"UNKNOWN",
            "market_regime":"SIDEWAYS",
            "breadth":"HẸP",
            "adv_ratio":0
        }

    up = 0

    for s in stocks:
        if s.get("change",0) > 0:
            up += 1

    ratio = up / len(stocks)

    if ratio > 0.65:
        regime = "UPTREND MẠNH"
        status = "RISK_ON"
        breadth = "THỊ TRƯỜNG RỘNG"

    elif ratio > 0.55:
        regime = "UPTREND"
        status = "RISK_ON"
        breadth = "KHÁ RỘNG"

    elif ratio > 0.45:
        regime = "SIDEWAYS"
        status = "TRUNG LẬP"
        breadth = "TRUNG BÌNH"

    else:
        regime = "DOWNTREND"
        status = "RISK_OFF"
        breadth = "THỊ TRƯỜNG HẸP"

    return {
        "market_status":status,
        "market_regime":regime,
        "breadth":breadth,
        "adv_ratio":round(ratio*100,1)
    }
