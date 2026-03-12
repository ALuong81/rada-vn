def detect_vcp(stock):

    if stock["volume"] < stock["avg_volume"]:

        return "CÓ"

    return "KHÔNG"
