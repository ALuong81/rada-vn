def breakout(stock):

    if stock["price"] > stock["resistance"]:

        return "VƯỢT ĐỈNH","XÁC SUẤT CAO"

    if stock["price"] > stock["resistance"]*0.95:

        return "Chuẩn bị breakout","XÁC SUẤT CAO"

    return "CHƯA SẴN SÀNG","THẤP"

def breakout_status(stock):

    price = stock.get("price",0)
    resistance = stock.get("resistance",0)

    if resistance == 0:
        return "ĐANG THEO DÕI"

    if price > resistance:
        return "VƯỢT ĐỈNH"

    if price > resistance * 0.97:
        return "CHUẨN BỊ BREAKOUT"

    if price > resistance * 0.9:
        return "PULLBACK TÍCH LŨY"

    return "ĐANG THEO DÕI"
