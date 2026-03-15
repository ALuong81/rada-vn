def super_sniper_selector(stocks):

    if not stocks:
        return []

    filtered = []

    for s in stocks:

        score = s.get("meta_score",0)

        breakout = s.get("breakout_prob",0)

        rs = s.get("rs_rating",0)

        if score > 80 and breakout > 60 and rs > 80:
            filtered.append(s)

    filtered = sorted(
        filtered,
        key=lambda x: x.get("meta_score",0),
        reverse=True
    )

    return filtered[:2]
