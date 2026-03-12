def vcp_pattern(stock):

    price = stock.get("price",0)
    resistance = stock.get("resistance",0)

    if resistance == 0:
        return False

    dist = price / resistance

    return 0.94 < dist < 1
