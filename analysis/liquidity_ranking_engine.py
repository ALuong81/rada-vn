def liquidity_ranking(stocks):

    filtered = []

    for s in stocks:

        volume = s.get("volume",0)
        avg_volume = s.get("avg_volume",0)

        if avg_volume > 500000:
            filtered.append(s)

    filtered = sorted(filtered, key=lambda x: x["avg_volume"], reverse=True)

    return filtered[:300]
