def vnindex_trend(index_data):

    """
    Xác định xu hướng VNINDEX
    """

    if not index_data or len(index_data) < 50:
        return "UNKNOWN"

    closes = [d.get("close", 0) for d in index_data]

    ma20 = sum(closes[-20:]) / 20
    ma50 = sum(closes[-50:]) / 50
    ma200 = sum(closes[-200:]) / 200
    
    last_close = closes[-1]

    if last_close > ma50 and ma50 > ma200:
        return "UPTREND"

    if last_close < ma200 and ma20 < ma50:
        return "DOWNTREND"

    return "SIDEWAY"
