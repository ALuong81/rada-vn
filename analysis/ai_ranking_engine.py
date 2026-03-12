def rank_stocks(stocks):

    for s in stocks:

        s["ai_score"]=s["meta_score"] + s["volume"]/10000

    ranked=sorted(stocks,key=lambda x:x["ai_score"],reverse=True)

    return ranked
