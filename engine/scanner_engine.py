import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from analysis.stock_universe_filter import get_stock_universe
from data.market_data import load_stock


MAX_WORKERS = 18


def scan_market():

    symbols = get_stock_universe()

    print("Universe loaded:", len(symbols))

    results = []

    start = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(load_stock, s): s
            for s in symbols
        }

        for future in as_completed(futures):

            symbol = futures[future]

            try:

                stock = future.result(timeout=20)

                if stock:
                    results.append(stock)

            except Exception as e:

                print("Load error:", symbol, e)

    print("Total stocks loaded:", len(results))

    print("Scan time:", round(time.time() - start, 2), "seconds")

    return results
