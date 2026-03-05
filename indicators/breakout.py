def breakout(df):

    high20 = df.high.rolling(20).max().iloc[-2]

    if df.close.iloc[-1] > high20:
        return True

    return False
