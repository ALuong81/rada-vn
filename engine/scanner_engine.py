from data.market_snapshot import get_market_snapshot

def scan_market():

    print("STEP 1: Scan market")

    stocks = get_market_snapshot()

    # nếu snapshot không có volume → load từng mã
    if stocks and "volume" not in stocks[0]:

        print("Snapshot has no data → loading symbols")

        symbols = [s["symbol"] for s in stocks]

        results = []

        with ThreadPoolExecutor(max_workers=18) as executor:

            futures = {
                executor.submit(load_stock, s): s
                for s in symbols
            }

            for f in as_completed(futures):

                data = f.result()

                if data:
                    results.append(data)

        stocks = results

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
