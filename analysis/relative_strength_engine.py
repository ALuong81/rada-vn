def relative_strength(stocks):

    if not stocks:
        return stocks

    avg_change = sum(s.get("change",0) for s in stocks) / len(stocks)

    for s in stocks:

        change = s.get("change",0)

        if change > avg_change * 2:
            s["rs_rating"] = "SIÊU MẠNH"

        elif change > avg_change:
            s["rs_rating"] = "MẠNH"

        elif change > 0:
            s["rs_rating"] = "TRUNG BÌNH"

        else:
            s["rs_rating"] = "YẾU"

    return stocks
