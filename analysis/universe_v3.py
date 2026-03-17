def build_universe_v3(stocks, top_n=50):

    if not stocks:
        return []

    for s in stocks:

        close = s.get("close", [])
        if len(close) < 20:
            continue

        recent = close[-20:]
        volat = (max(recent) - min(recent)) / max(recent)

        s["volatility"] = volat

    stocks.sort(
        key=lambda x: (
            x.get("avg_volume", 0),
            x.get("volatility", 0)
        ),
        reverse=True
    )

    return stocks[:top_n]
