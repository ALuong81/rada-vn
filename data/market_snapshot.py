import requests


def get_market_snapshot():

    url = "https://iboard.ssi.com.vn/dchart/api/v1/all"

    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        print("Market API error")
        return []

    data = r.json()

    stocks = []

    for s in data:

        try:

            symbol = s["symbol"]

            if len(symbol) > 3:
                continue

            price = float(s["close"])
            volume = float(s["volume"])

            stocks.append({
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "avg_volume": volume,
                "change": s.get("changePercent", 0)
            })

        except:
            continue

    print("Market snapshot:", len(stocks))

    return stocks
