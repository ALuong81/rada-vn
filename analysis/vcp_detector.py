def vcp_pattern(stocks):

    for s in stocks:

        price = s.get("price", 0)
        resistance = s.get("resistance", 0)
        volume = s.get("volume", 0)
        avg_volume = s.get("avg_volume", 0)

        if resistance == 0:
            s["vcp"] = "KHÔNG"
            continue

        # giá đang co gần kháng cự
        tight_price = price > resistance * 0.85

        # volume đang giảm
        dry_volume = volume < avg_volume * 0.8

        if tight_price and dry_volume:
            s["vcp"] = "CÓ"
        else:
            s["vcp"] = "KHÔNG"

    return stocks
    
def scan_vcp(stocks):

    for s in stocks:
        detect_vcp(s)

    return stocks
