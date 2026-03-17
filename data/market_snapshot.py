import requests
from vnstock import listing_companies


def api_ssi():

    try:

        url = "https://iboard.ssi.com.vn/dchart/api/v1/all"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()

        stocks = []

        for s in data:

            symbol = s.get("symbol")

            if not symbol or len(symbol) > 3:
                continue

            price = float(s.get("close", 0))
            volume = float(s.get("volume", 0))

            stocks.append({
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "avg_volume": volume,
                "change": s.get("changePercent", 0)
            })

        print("SSI snapshot:", len(stocks))

        return stocks

    except Exception as e:

        print("SSI API failed:", e)

        return []


def api_vndirect():

    try:

        url = "https://api-finfo.vndirect.com.vn/v4/stock_prices"

        params = {
            "q": "code:~AAA",
            "size": 2000
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()

        stocks = []

        for s in data.get("data", []):

            symbol = s.get("code")

            if not symbol or len(symbol) > 3:
                continue

            price = float(s.get("close", 0))
            volume = float(s.get("nmVolume", 0))

            stocks.append({
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "avg_volume": volume,
                "change": s.get("changePct", 0)
            })

        print("VNDIRECT snapshot:", len(stocks))

        return stocks

    except Exception as e:

        print("VNDIRECT API failed:", e)

        return []


def api_symbols():

    try:

        df = listing_companies()

        if df is None:
            return []

        symbols = df["ticker"].dropna().tolist()

        stocks = []

        for s in symbols:

            if isinstance(s, str) and 2 <= len(s.strip()) <= 3:

                stocks.append({
                    "symbol": s.strip().upper()
                })

        print("Fallback symbols:", len(stocks))

        return stocks

    except Exception as e:

        print("Symbol fallback failed:", e)

        return []


def get_market_snapshot():

    print("Fetching market snapshot")

    stocks = api_ssi()

    if stocks:
        print("SSI")
        return stocks

    stocks = api_vndirect()

    if stocks:
        print("VND")
        return stocks
        

    return api_symbols()
