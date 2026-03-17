def multi_tf_trend(s):

    close = s.get("close")

    if close is None or len(close) < 50:
        return "UNKNOWN"

    try:

        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()

        last = float(close.iloc[-1])
        ma20_last = float(ma20.iloc[-1])
        ma50_last = float(ma50.iloc[-1])

        if last > ma20_last > ma50_last:
            return "UPTREND"

        elif last < ma20_last < ma50_last:
            return "DOWNTREND"

        return "SIDEWAY"

    except:
        return "UNKNOWN"
