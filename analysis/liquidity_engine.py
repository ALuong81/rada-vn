def liquidity_signal(s):

    volume = s.get("volume")

    if volume is None:
        return 0

    try:

        avg = float(volume.tail(20).mean())
        last = float(volume.iloc[-1])

        return last / avg if avg > 0 else 0

    except:
        return 0
