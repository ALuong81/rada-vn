def breakout(stock):

    if stock["price"] > stock["resistance"]:

        return "VƯỢT ĐỈNH","XÁC SUẤT CAO"

    if stock["price"] > stock["resistance"]*0.98:

        return "Chuẩn bị breakout","XÁC SUẤT CAO"

    return "CHƯA SẴN SÀNG","THẤP"
