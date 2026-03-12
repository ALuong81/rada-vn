def multi_tf_trend(stock):

    change = stock.get("change",0)

    if change > 3:
        return "ĐỒNG THUẬN MẠNH"

    if change > 1:
        return "ĐỒNG THUẬN"

    if change > -1:
        return "TRUNG TÍNH"

    return "YẾU"
