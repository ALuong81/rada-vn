def sector_strength(stocks):

    sectors = {}

    for s in stocks:

        sector = s.get("sector","UNKNOWN")
        change = s.get("change",0)

        sectors.setdefault(sector,[]).append(change)

    strength = {}

    for k,v in sectors.items():

        strength[k] = sum(v)/len(v)

    return strength
