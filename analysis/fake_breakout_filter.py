def filter_fake_breakout(stocks):

    filtered = []

    for s in stocks:

        price = s.get("price", 0)
        resistance = s.get("resistance", 0)
        volume = s.get("volume", 0)
        avg = s.get("avg_volume", 0)

        if resistance == 0:
            continue

        breakout = price > resistance * 0.98

        vol_ok = volume > avg * 1.2

        if breakout and vol_ok:
            filtered.append(s)

    return filtered
