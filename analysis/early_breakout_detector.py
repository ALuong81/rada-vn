def early_breakout(s):

    price = s.get("price",0)
    ma20 = s.get("ma20",0)
    volume = s.get("volume",0)
    avg_volume = s.get("avg_volume",0)

    if not ma20:
        return False

    near_resistance = price > ma20 * 0.98

    volume_pickup = volume > avg_volume * 1.2

    if near_resistance and volume_pickup:
        return True

    return False
