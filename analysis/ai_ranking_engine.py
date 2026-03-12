def rank_stocks(stocks):

    for s in stocks:

        meta = s.get("meta_score", 0)
        vol = s.get("volume", 0)
        s["ai_score"] = meta + vol/10000

    ranked=sorted(stocks,key=lambda x:x["ai_score"],reverse=True)

    return ranked
