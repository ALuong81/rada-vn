def build_universe_v3(stocks, top_n=80):

    filtered = []

    for s in stocks:

        try:
            vol = s.get("avg_volume", 0)
            price = s.get("price", 0)
            close = s.get("close", [])

            if vol < 100000:
                continue

            if price < 5 or price > 200:
                continue

            if len(close) < 20:
                continue

            recent = close[-20:]
            volat = (max(recent) - min(recent)) / max(recent)

            if volat < 0.05:
                continue

            s["volatility"] = volat

            filtered.append(s)

        except:
            continue

    filtered.sort(
        key=lambda x: (
            x.get("avg_volume", 0),
            x.get("volatility", 0)
        ),
        reverse=True
    )

    return filtered[:top_n]
