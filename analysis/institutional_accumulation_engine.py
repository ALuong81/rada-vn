def institutional_accumulation(stock):

    volume = stock.get("volume",0)
    avg_volume = stock.get("avg_volume",1)
    change = stock.get("change",0)

    if volume > avg_volume*2 and change > 2:
        return "QUỸ GOM MẠNH"

    if volume > avg_volume*1.5 and change > 0:
        return "CÓ DẤU HIỆU"

    return "KHÔNG"
