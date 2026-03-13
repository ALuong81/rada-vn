def institutional_flow(stock):

    volume = stock.get("volume", 0)
    avg_volume = stock.get("avg_volume", 1)
    change = stock.get("change", 0)

    if volume > avg_volume * 2 and change > 1:
        return "QUY MUA MANH"

    if volume > avg_volume * 1.5:
        return "CO DONG TIEN"

    return "KHONG RO"
