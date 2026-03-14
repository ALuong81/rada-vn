import pandas as pd


def liquidity_signal(stock):

    df = stock.get("data")

    if df is None or len(df) < 30:
        return "BÌNH THƯỜNG"

    vol = df["volume"]

    avg20 = vol.tail(20).mean()
    today = vol.iloc[-1]

    if today > avg20 * 2:
        return "DÒNG TIỀN LỚN"

    if today > avg20 * 1.3:
        return "DÒNG TIỀN TĂNG"

    return "BÌNH THƯỜNG"
