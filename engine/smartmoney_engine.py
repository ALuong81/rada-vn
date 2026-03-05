def liquidity_grab(df):

    low = df.low.iloc[-1]

    prev = df.low.iloc[-5:-1].min()

    if low < prev:
        return True

    return False
