from data.market_snapshot import get_market_snapshot


def scan_market():

    print("STEP 1: Scan market")

    stocks = get_market_snapshot()

    results = []

    for s in stocks:

        # lọc thanh khoản
        if s["volume"] < 200000:
            continue

        # lọc penny
        if s["price"] < 3:
            continue

        results.append(s)

    print("Tradable stocks:", len(results))

    return results
