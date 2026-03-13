def distribution_day(index_data):

    if len(index_data) < 2:
        return False

    today = index_data[-1]
    yesterday = index_data[-2]

    price_down = today["close"] < yesterday["close"]
    volume_up = today["volume"] > yesterday["volume"]

    if price_down and volume_up:
        return True

    return False
