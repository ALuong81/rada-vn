def detect_wyckoff(df):

    vol = df.volume

    acc = vol.iloc[-10:].mean() > vol.iloc[-30:].mean()

    if acc:
        return "Accumulation"

    return "None"
