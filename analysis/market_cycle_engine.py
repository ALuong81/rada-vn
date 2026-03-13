def market_cycle(stock):

    price = stock.get("price", 0)
    resistance = stock.get("resistance", 0)
    change = stock.get("change", 0)

    if price > resistance * 0.95 and change > 0:
        return "MARKUP"

    if change > 0 and price < resistance * 0.9:
        return "ACCUMULATION"

    if change < -2:
        return "MARKDOWN"

    return "SIDEWAY"
