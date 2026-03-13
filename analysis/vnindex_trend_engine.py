def vnindex_trend(index):

    close = index.get("close",0)
    ma50 = index.get("ma50",0)
    ma200 = index.get("ma200",0)

    if close > ma50 and ma50 > ma200:
        return "UPTREND"

    if close < ma50 and ma50 < ma200:
        return "DOWNTREND"

    return "SIDEWAY"
