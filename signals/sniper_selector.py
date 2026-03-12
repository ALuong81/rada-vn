def select_sniper(stocks):

    if not stocks:
        return []

    # lọc cổ phiếu đạt ngưỡng meta score
    candidates = [s for s in stocks if s.get("meta_score", 0) >= 60]

    # nếu không có sniper thì fallback top momentum
    if not candidates:
        stocks = sorted(stocks, key=lambda x: x.get("change", 0), reverse=True)
        return stocks[:3]

    # sắp xếp theo ai_score
    candidates = sorted(candidates, key=lambda x: x.get("ai_score", 0), reverse=True)

    return candidates[:5]
