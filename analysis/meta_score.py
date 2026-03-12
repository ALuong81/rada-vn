def score_stock(stock):

    score = 0

    volume = stock.get("volume", 0)
    avg_volume = stock.get("avg_volume", 0)
    price = stock.get("price", 0)
    resistance = stock.get("resistance", 0)

    # breakout strength
    if price > resistance * 0.97:
        score += 40

    # volume expansion
    if avg_volume > 0 and volume > avg_volume * 1.5:
        score += 40

    # supply dry-up
    if avg_volume > 0 and volume < avg_volume * 0.7:
        score += 30

    return score
