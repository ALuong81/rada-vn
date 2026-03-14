def sector_momentum(stocks):

    sector_score = {}

    for s in stocks:

        sector = s.get("sector")

        if not sector:
            continue

        score = s.get("meta_score", 0)

        sector_score.setdefault(sector, []).append(score)

    momentum = []

    for sector, scores in sector_score.items():

        avg = sum(scores) / len(scores)

        momentum.append((sector, avg))

    momentum.sort(key=lambda x: x[1], reverse=True)

    return momentum
