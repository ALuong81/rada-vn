def liquidity_ok(stock):

    vol = stock.get("volume",0)
    avg = stock.get("avg_volume",0)

    if avg == 0:
        return False

    if avg < 100000:
        return False

    if vol < avg * 0.5:
        return False

    return True
