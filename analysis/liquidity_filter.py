def liquidity_filter(stocks):

    filtered = []

    for s in stocks:

        price = s.get("price", 0)
        avg_volume = s.get("avg_volume", 0)

        # tiêu chuẩn thanh khoản
        if price < 8:
            continue

        if avg_volume < 200000:
            continue

        filtered.append(s)

    return filtered
