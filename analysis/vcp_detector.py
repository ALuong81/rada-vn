def detect_vcp(stock):

    price = stock.get("price", 0)
    resistance = stock.get("resistance", 0)
    volume = stock.get("volume", 0)
    avg = stock.get("avg_volume", 0)

    if resistance == 0:
        stock["vcp"] = False
        return stock

    tight_range = price > resistance * 0.85

    volume_dry = volume < avg * 0.8

    if tight_range and volume_dry:
        stock["vcp"] = True
    else:
        stock["vcp"] = False

    return stock


def scan_vcp(stocks):

    for s in stocks:
        detect_vcp(s)

    return stocks
