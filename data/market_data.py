from vnstock import Vnstock
from .cache_layer import get_cache, set_cache

vnstock = Vnstock()

def get_symbols():

    listing = vnstock.stock.listing.symbols_by_exchange()

    hose = listing["HOSE"]
    hnx = listing["HNX"]
    upcom = listing["UPCOM"]

    symbols = hose + hnx + upcom

    return symbols


def load_stock(symbol):

    cache = get_cache(symbol)

    if cache:
        return cache

    df = vnstock.stock.quote.history(
        symbol=symbol,
        start="2024-01-01"
    )

    price = float(df.close.iloc[-1])

    data = {

        "symbol": symbol,
        "price": price,
        "volume": float(df.volume.iloc[-1]),
        "avg_volume": float(df.volume.tail(20).mean()),
        "resistance": float(df.close.tail(50).max()),
        "change": float(df.close.pct_change().iloc[-1] * 100)

    }

    set_cache(symbol, data)

    return data
