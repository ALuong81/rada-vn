from concurrent.futures import ThreadPoolExecutor, as_completed
from data.market_data import get_symbols, load_stock


MAX_WORKERS = 6


def scan_market():

    symbols = get_symbols()

    if not symbols:
        return []

    # ✅ giới hạn để tránh overload
    symbols = symbols[:120]

    print("Symbols to load:", len(symbols))

    results = []
    total = len(symbols)

    print("Start loading...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(load_stock, s): s
            for s in symbols
        }

        for i, future in enumerate(as_completed(futures), 1):

            try:
                stock = future.result(timeout=10)

                # ✅ filter cơ bản ngay tại đây
                if stock and stock.get("avg_volume", 0) > 50000:
                    results.append(stock)

            except Exception:
                pass

            if i % 10 == 0:
                print(f"Progress {i}/{total}")

    print(f"Loaded OK: {len(results)} | Failed: {total - len(results)}")

    return results
