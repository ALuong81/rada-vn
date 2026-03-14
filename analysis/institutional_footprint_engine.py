def institutional_footprint(stock):

    df = stock.get("data")

    if df is None or len(df) < 40:
        return "KHÔNG"

    close = df["close"]
    volume = df["volume"]

    up_days = 0
    down_days = 0

    for i in range(-10, -1):

        if close.iloc[i] > close.iloc[i-1] and volume.iloc[i] > volume.iloc[i-1]:
            up_days += 1

        if close.iloc[i] < close.iloc[i-1] and volume.iloc[i] > volume.iloc[i-1]:
            down_days += 1

    if up_days >= 5 and down_days <= 1:
        return "QUỸ GOM MẠNH"

    if up_days >= 3:
        return "QUỸ GOM"

    return "KHÔNG"
