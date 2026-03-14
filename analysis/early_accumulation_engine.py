def early_accumulation(stock):

    df = stock.get("data")

    if df is None or len(df) < 40:
        return False

    close = df["close"]
    volume = df["volume"]

    price_range = close.tail(15).max() - close.tail(15).min()

    avg_vol = volume.tail(20).mean()
    recent_vol = volume.tail(5).mean()

    # giá đi ngang + volume giảm
    if price_range / close.iloc[-1] < 0.05 and recent_vol < avg_vol * 0.8:
        return True

    return False
