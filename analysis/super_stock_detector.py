def detect_super_stock(stock):

    price = stock.get("price", 0)
    resistance = stock.get("resistance", 0)
    volume = stock.get("volume", 0)
    avg_volume = stock.get("avg_volume", 0)
    trend = stock.get("trend", "")
    leader = stock.get("leader", "KHÔNG")
    vcp = stock.get("vcp", False)

    score = 0

    # giá gần đỉnh
    if resistance and price > resistance * 0.85:
        score += 1

    # volume lớn
    if avg_volume and volume > avg_volume * 1.5:
        score += 1

    # xu hướng mạnh
    if trend == "ĐỒNG THUẬN MẠNH":
        score += 1

    # leader ngành
    if leader == "CÓ":
        score += 1

    # có VCP
    if vcp:
        score += 1

    if score >= 4:
        stock["super_stock"] = "SIÊU CỔ PHIẾU"
    elif score >= 3:
        stock["super_stock"] = "TIỀM NĂNG"
    else:
        stock["super_stock"] = "BÌNH THƯỜNG"

    stock["super_score"] = score

    return stock


def scan_super_stocks(stocks):

    results = []

    for s in stocks:

        if not isinstance(s, dict):
            continue

        s = detect_super_stock(s)

        results.append(s)

    return results
