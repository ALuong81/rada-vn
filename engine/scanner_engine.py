import time
from concurrent.futures import ThreadPoolExecutor
from data.market_data import load_stock, get_symbols
from config import THREAD_WORKERS


def scan_market():

    symbols = get_symbols()
    print("Loaded symbols:", len(symbols))
    stocks = []

def worker(symbol):

    try:

        s = load_stock(symbol)

        if s:
            stocks.append(s)

    except Exception as e:

        print("Error:", symbol, e)

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as exe:

        exe.map(worker, symbols)

    return stocks
