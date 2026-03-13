def detect_pattern(stock):

    change = stock.get("change",0)
    volume = stock.get("volume",0)
    avg_volume = stock.get("avg_volume",1)

    if change > 3 and volume > avg_volume*2:
        return "BREAKOUT PATTERN"

    if change > 1 and volume < avg_volume:
        return "TIGHT CONSOLIDATION"

    return "NO PATTERN"
