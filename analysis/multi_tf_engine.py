def multi_tf(stock):

    if stock["price"] > stock["resistance"]*0.9:

        return "ĐỒNG THUẬN MẠNH"

    return "TRUNG LẬP"
