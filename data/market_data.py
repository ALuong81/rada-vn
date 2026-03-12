from vnstock import stock_historical_data, listing_companies
from .cache_layer import get_cache, set_cache


def get_symbols():

    try:

        hose = listing_companies()
        symbols = list(hose["ticker"])

        return symbols

    except:

        # fallback nếu API thay đổi
        return []


def load_stock(symbol):

    cache = get_cache(symbol)

    if cache:
        return cache

    df = stock_historical_data(
        symbol=symbol,
        start_date="2024-01-01",
        end_date=None
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
