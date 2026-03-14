def market_leader(stock):

    """
    Xác định cổ phiếu dẫn dắt ngành
    """

    rs = stock.get("rs_rating", "")
    meta = stock.get("meta_score", 0)
    volume = stock.get("volume_ratio", 1)

    if rs == "SIÊU MẠNH" and meta > 80 and volume > 1.2:
        return "CÓ"

    if rs == "MẠNH" and meta > 70:
        return "CÓ"

    return "KHÔNG"
