from concurrent.futures import ThreadPoolExecutor, as_completed

from data.market_snapshot import get_market_snapshot
from data.market_data import load_stock


MAX_WORKERS = 20
MAX_SYMBOLS = 400


def scan_market():

    print("STEP 1: Scan market")

    # -------------------------------------------------
    # 1. Lấy snapshot thị trường
    # -------------------------------------------------

    print("Fetching market snapshot")

    stocks = get_market_snapshot()

    # -------------------------------------------------
    # 2. Nếu snapshot chỉ có symbol → load từng mã
    # -------------------------------------------------

    if stocks and "volume" not in stocks[0]:

        print("Snapshot has no data → loading symbols")

        symbols = [s["symbol"] for s in stocks][:MAX_SYMBOLS]

        print("Symbols to load:", len(symbols))

        results = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            futures = {
                executor.submit(load_stock, s): s
                for s in symbols
            }

            total = len(symbols)

            for i, future in enumerate(as_completed(futures), 1):

                try:

                    data = future.result()

                    if data:
                        results.append(data)

                except Exception:
                    pass

                # log progress
                if i % 50 == 0:
                    print(f"Progress {i}/{total}")

        stocks = results

    if not stocks:
        print("No market data loaded")
        return []

    # -------------------------------------------------
    # 3. Lọc cổ phiếu tradable
    # -------------------------------------------------

    tradable = []

    for s in stocks:

        volume = s.get("volume", 0)
        price = s.get("price", 0)

        if volume < 200000:
            continue

        if price < 3:
            continue

        tradable.append(s)

    print("Tradable stocks:", len(tradable))

    return tradable
