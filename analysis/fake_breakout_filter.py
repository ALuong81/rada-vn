def fake_breakout_filter(stock):

    if stock["volume"] < stock["avg_volume"] * 0.7:

        return True

    return False
