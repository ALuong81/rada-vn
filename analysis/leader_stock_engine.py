def detect_leaders(stocks):

    sector_best = {}

    for s in stocks:

        sector = s.get("sector", "KHÁC")

        score = s.get("meta_score", 0)

        if sector not in sector_best:
            sector_best[sector] = s

        elif score > sector_best[sector].get("meta_score", 0):
            sector_best[sector] = s

    leaders = set()

    for s in sector_best.values():
        leaders.add(s["symbol"])

    for s in stocks:

        if s["symbol"] in leaders:
            s["leader"] = "CÓ"
        else:
            s["leader"] = "KHÔNG"

    return stocks
