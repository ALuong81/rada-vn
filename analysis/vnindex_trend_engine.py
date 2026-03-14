def vnindex_trend(index_data):

    """
    Xác định xu hướng VNINDEX
    """

    if not index_data or len(index_data) < 60:
        return "UNKNOWN"

    closes = [d.get("close", 0) for d in index_data]

    ma20 = sum(closes[-20:]) / 20
    ma50 = sum(closes[-50:]) / 50
    ma200 = sum(closes[-200:]) / 200 if len(closes) >= 200 else ma50
    
    last_close = closes[-1]

    if last_close > ma20 > ma50 > ma200:
        return "UPTREND"

    if last_close <  ma20 < ma50:
        return "DOWNTREND"

    if ma20 > ma50 and last_close < ma20:
        return "PULLBACK"

    return "SIDEWAY"
