def fake_breakout_filter(stock):

    if stock["volume"] < stock["avg_volume"]:

        return True

    return False
