def sector_rotation_pro(stocks):

    sector_perf = {}

    for s in stocks:

        sector = s.get("sector","UNKNOWN")
        change = s.get("change",0)

        if sector not in sector_perf:
            sector_perf[sector] = []

        sector_perf[sector].append(change)

    sector_strength = []

    for sec,values in sector_perf.items():

        avg = sum(values)/len(values)
        sector_strength.append((sec,avg))

    sector_strength.sort(key=lambda x:x[1], reverse=True)

    strong = sector_strength[:3]
    weak = sector_strength[-3:]

    return strong, weak
