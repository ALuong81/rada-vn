import requests

CACHE = None


def get_market_snapshot():

    global CACHE

    if CACHE:
        return CACHE

    url = "https://api.vndirect.com.vn/v4/stock_prices"

    params = {
        "q": "code:~AAA",
        "size": 2000
    }

    r = requests.get(url, params=params)

    if r.status_code != 200:
        return []

    data = r.json()

    stocks = []

    for s in data.get("data", []):

        try:

            stock = {
                "symbol": s["code"],
                "price": float(s["close"]),
                "volume": float(s["nmVolume"]),
                "avg_volume": float(s["nmVolume"]),
                "change": float(s["changePct"])
            }

            stocks.append(stock)

        except:
            continue

    CACHE = stocks

    print("Market snapshot:", len(stocks))

    return stocks
