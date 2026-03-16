import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from analysis.stock_universe_filter import get_stock_universe
from data.market_data import load_stock

MAX_WORKERS = 12


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

        done = 0

        for future in as_completed(futures):

            symbol = futures[future]

            try:

                stock = future.result(timeout=15)

                if stock:
                    results.append(stock)

            except Exception as e:

                print("Load error:", symbol)

            done += 1

            if done % 50 == 0:
                print(f"Progress {done}/{len(symbols)}")

    print("Total stocks loaded:", len(results))

    print("Scan time:", round(time.time() - start, 2), "seconds")

    return results
