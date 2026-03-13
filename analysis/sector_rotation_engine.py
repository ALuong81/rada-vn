from .sector_map import SECTOR_MAP


def detect_sector(symbol):

    if not isinstance(symbol, str):
        return "KHÁC"

    return SECTOR_MAP.get(symbol, "KHÁC")


def sector_rotation(stocks):

    sector_strength = {}

    for s in stocks:

        if not isinstance(s, dict):
            continue

        symbol = s.get("symbol")

        sector = detect_sector(symbol)

        s["sector"] = sector

        change = s.get("change", 0)

        sector_strength[sector] = sector_strength.get(sector, 0) + change

    if not sector_strength:
        return stocks

    leader_sector = max(sector_strength, key=sector_strength.get)

    for s in stocks:

        if s.get("sector") == leader_sector:
            s["sector_leader"] = "CÓ"
        else:
            s["sector_leader"] = "KHÔNG"

    return stocks
