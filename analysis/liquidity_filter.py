def liquidity_filter(stock):

    if stock["avg_volume"] < 100000:

        return False

    return True
