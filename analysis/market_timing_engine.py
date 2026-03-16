def market_timing_engine(index_data):

    if not index_data or len(index_data) < 50:
        return {
            "timing": "UNKNOWN",
            "distribution_days": 0,
            "follow_through": False,
            "rally_attempt": False
        }

    data = index_data[-50:]

    distribution_days = 0
    follow_through = False
    rally_attempt = False

    rally_day = 0

    for i in range(1, len(data)):

        today = data[i]
        prev = data[i-1]

        close_today = today.get("close",0)
        close_prev = prev.get("close",0)

        vol_today = today.get("volume",0)
        vol_prev = prev.get("volume",0)

        if close_prev == 0:
            continue

        change = (close_today - close_prev) / close_prev

        # Distribution Day
        if change < -0.002 and vol_today > vol_prev:
            distribution_days += 1

        # Rally attempt
        if change > 0:
            rally_day += 1
        else:
            rally_day = 0

        if rally_day >= 3:
            rally_attempt = True

        # Follow Through Day
        if rally_day >= 4 and change > 0.015 and vol_today > vol_prev:
            follow_through = True

    # Market state
    if distribution_days >= 5:
        timing = "MARKET IN CORRECTION"

    elif follow_through:
        timing = "CONFIRMED UPTREND"

    elif rally_attempt:
        timing = "RALLY ATTEMPT"

    else:
        timing = "MARKET UNDER PRESSURE"

    return {
        "timing": timing,
        "distribution_days": distribution_days,
        "follow_through": follow_through,
        "rally_attempt": rally_attempt
    }
