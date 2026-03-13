def market_timing(index_data):

    if len(index_data) < 5:
        return "UNKNOWN"

    distribution_days = 0
    follow_through = False

    for i in range(1, len(index_data)):

        today = index_data[i]
        prev = index_data[i-1]

        price_down = today["close"] < prev["close"]
        volume_up = today["volume"] > prev["volume"]

        # distribution day
        if price_down and volume_up:
            distribution_days += 1

        # follow through day
        price_up_big = today["close"] > prev["close"] * 1.015
        volume_strong = today["volume"] > prev["volume"]

        if price_up_big and volume_strong:
            follow_through = True

    if distribution_days >= 4:
        return "MARKET IN CORRECTION"

    if follow_through:
        return "CONFIRMED UPTREND"

    return "MARKET UNDER PRESSURE"
