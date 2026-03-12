from vnstock import *
from .cache_layer import get_cache,set_cache


def get_symbols():

    hose = listing_companies(exchange='HOSE')
    hnx = listing_companies(exchange='HNX')
    upcom = listing_companies(exchange='UPCOM')

    symbols = list(hose['ticker']) + list(hnx['ticker']) + list(upcom['ticker'])

    return symbols


def load_stock(symbol):

    cache=get_cache(symbol)

    if cache:
        return cache

    df = stock_historical_data(symbol,"2024-01-01")

    price = df.close.iloc[-1]

    data = {

        "symbol":symbol,
        "price":price,
        "volume":df.volume.iloc[-1],
        "avg_volume":df.volume.tail(20).mean(),
        "resistance":df.close.tail(50).max(),
        "change":df.close.pct_change().iloc[-1]*100

    }

    set_cache(symbol,data)

    return data
