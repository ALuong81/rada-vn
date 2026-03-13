def breakout_probability(stock):

    score = 0

    if stock.get("vcp"):
        score += 30

    if stock.get("accumulation"):
        score += 25

    if stock.get("relative_strength") == "SIÊU MẠNH":
        score += 25

    if stock.get("smart_money"):
        score += 20

    if score >= 80:
        return "RẤT CAO"

    if score >= 60:
        return "CAO"

    if score >= 40:
        return "TRUNG BÌNH"

    return "THẤP"
