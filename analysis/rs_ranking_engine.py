def rs_score(stock):

    change = stock.get("change",0)

    return change*10
