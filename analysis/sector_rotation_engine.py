from .sector_map import SECTOR_MAP


def detect_sector(symbol):

    return SECTOR_MAP.get(symbol, "KHÁC")


def sector_rotation(stocks):

    sector_strength = {}

    for s in stocks:

        sector = detect_sector(s["symbol"])

        s["sector"] = sector

        if sector not in sector_strength:
            sector_strength[sector] = 0

        sector_strength[sector] += s.get("change", 0)

    if not sector_strength:
        return stocks

    leader_sector = max(sector_strength, key=sector_strength.get)

    for s in stocks:

        if s["sector"] == leader_sector:
            s["sector_leader"] = "CÓ"
        else:
            s["sector_leader"] = "KHÔNG"

    return stocks
