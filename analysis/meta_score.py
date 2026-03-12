def score_stock(s):

    score = 0

    price = s.get("price",0)
    resistance = s.get("resistance",0)
    volume = s.get("volume",0)
    avg_volume = s.get("avg_volume",0)
    change = s.get("change",0)

    # breakout proximity
    if resistance > 0:
        dist = price / resistance

        if dist > 1:
            score += 60
        elif dist > 0.98:
            score += 40
        elif dist > 0.95:
            score += 20

    # volume expansion
    if avg_volume > 0:
        vol_ratio = volume / avg_volume

        if vol_ratio > 2:
            score += 40
        elif vol_ratio > 1.5:
            score += 30
        elif vol_ratio > 1.2:
            score += 20

    # momentum
    if change > 3:
        score += 20
    elif change > 1:
        score += 10

    return score
