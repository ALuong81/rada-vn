def meta_score(stock):

    score=0

    if stock["volume"]>stock["avg_volume"]*1.5:
        score+=40

    if stock["price"]>stock["resistance"]*0.95:
        score+=40

    if stock["volume"]<stock["avg_volume"]*0.7:
        score+=30

    return score
