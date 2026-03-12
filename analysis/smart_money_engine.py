def smart_money(stock):

    vol = stock.get("volume",0)
    avg = stock.get("avg_volume",0)

    if avg == 0:
        return False

    if vol > avg * 1.8:
        return True

    return False
