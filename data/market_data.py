from vnstock import stock_historical_data
from .cache_layer import get_cache, set_cache

def get_symbols():

    try:

        df = listing_companies()

        if df is None or len(df) == 0:
            return []

        symbols = df["ticker"].dropna().tolist()

        return symbols

    except Exception as e:

        print("Error loading symbols:", e)

        return []
    

def load_stock(symbol):

    cache = get_cache(symbol)

    if cache:
        return cache

    try:

        df = stock_historical_data(
            symbol=symbol,
            start_date="2024-01-01",
            end_date="2026-12-31",
            resolution="1D"
        )

        if df is None or len(df) < 60:
            return None

        price = float(df["close"].iloc[-1])
        volume = float(df["volume"].iloc[-1])
        avg_volume = float(df["volume"].tail(20).mean())
        resistance = float(df["close"].tail(50).max())
        change = float(df["close"].pct_change().iloc[-1] * 100)

        data = {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "avg_volume": avg_volume,
            "resistance": resistance,
            "change": change
        }

        set_cache(symbol, data)

        return data

    except Exception as e:

        print("Error loading", symbol, e)

        return None
