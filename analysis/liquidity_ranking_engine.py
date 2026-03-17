def liquidity_ranking(stocks):

    if not stocks:
        return []

    for s in stocks:
        s["liquidity_score"] = s.get("avg_volume", 0)

    stocks.sort(
        key=lambda x: x.get("liquidity_score", 0),
        reverse=True
    )

    # ❗ KHÔNG filter chết nữa
    return stocks[:30]
