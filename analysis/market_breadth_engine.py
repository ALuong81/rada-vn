def analyze_market(stocks):

    if not stocks:
        return {
            "status": "UNKNOWN",
            "mode": "UNKNOWN",
            "breadth": "UNKNOWN",
            "adv_ratio": 0
        }

    adv = sum(1 for s in stocks if s.get("change",0) > 0)
    dec = sum(1 for s in stocks if s.get("change",0) <= 0)

    total = adv + dec

    if total == 0:
        ratio = 0
    else:
        ratio = adv / total * 100

    # breadth
    if ratio > 60:
        breadth = "THỊ TRƯỜNG RỘNG"
    else:
        breadth = "THỊ TRƯỜNG HẸP"

    # market status
    if ratio > 65:
        status = "RISK ON"
    else:
        status = "RISK OFF"

    # market mode
    if ratio > 60:
        mode = "UPTREND"
    elif ratio < 40:
        mode = "DOWNTREND"
    else:
        mode = "SIDEWAYS"

    return {
        "status": status,
        "mode": mode,
        "breadth": breadth,
        "adv_ratio": round(ratio,1)
    }
