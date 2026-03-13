def sector_heatmap(stocks):

    sectors = {}

    for s in stocks:

        sector = s.get("sector","UNKNOWN")
        change = s.get("change",0)

        sectors.setdefault(sector,[]).append(change)

    sector_score = {}

    for k,v in sectors.items():

        score = sum(v)/len(v)

        sector_score[k] = score

    ranked = sorted(sector_score.items(), key=lambda x:x[1], reverse=True)

    return ranked
