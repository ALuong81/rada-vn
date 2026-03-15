def super_sniper_selector(stocks):

    if not stocks:
        return []

    filtered = []

    for s in stocks:

        try:
            score = float(s.get("meta_score",0))
        except:
            score = 0

        try:
            breakout = float(s.get("breakout_prob",0))
        except:
            breakout = 0

        try:
            rs = float(s.get("rs_rating",0))
        except:
            rs = 0

        if score > 80 and breakout > 60 and rs > 80:
            filtered.append(s)

    filtered = sorted(
        filtered,
        key=lambda x: float(x.get("meta_score",0)),
        reverse=True
    )

    return filtered[:2]
