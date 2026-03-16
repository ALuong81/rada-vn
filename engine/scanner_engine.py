import time
from config import THREAD_WORKERS
from data.market_data import get_symbols, load_stock
from concurrent.futures import ThreadPoolExecutor, as_completed
from analysis.stock_universe_filter import get_stock_universe


MAX_WORKERS = 20


def scan_market():

    #symbols = get_symbols()
    symbols = get_stock_universe()

    print("Loaded symbols:", len(symbols))

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(load_stock, s): s
            for s in symbols
        }

        for future in as_completed(futures):

            try:

                stock = future.result()

                if stock:
                    results.append(stock)

            except Exception:
                pass

    print("Total stocks:", len(results))

    return results
