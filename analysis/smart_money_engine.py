def smart_money(stock):

    if stock["volume"] > stock["avg_volume"]*1.5:

        return "CÓ"

    return "KHÔNG"
