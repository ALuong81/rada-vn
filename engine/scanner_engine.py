from concurrent.futures import ThreadPoolExecutor, as_completed
from data.market_data import load_stock
from analysis.stock_universe_filter import get_stock_universe


MAX_WORKERS = 6


def scan_market():

    symbols = get_stock_universe()

    # chỉ lấy top để tránh nghẽn API
    symbols = symbols[:120]

    print("Symbols to load:", len(symbols))

    results = []
    total = len(symbols)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {executor.submit(load_stock, s): s for s in symbols}

        for i, future in enumerate(as_completed(futures), 1):

            try:
                stock = future.result()

                if stock:
                    results.append(stock)

            except:
                pass

            if i % 20 == 0:
                print(f"Progress {i}/{total}")

    fail = total - len(results)

    print(f"Loaded OK: {len(results)} | Failed: {fail}")

    return results
