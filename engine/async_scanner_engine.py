import asyncio
from data.market_data import get_symbols
from data.async_market_data import fetch_stock, MAX_CONCURRENT


async def scan_market_async():

    symbols = get_symbols()

    if not symbols:
        return []

    symbols = symbols[:120]

    print("Symbols to load:", len(symbols))

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    tasks = [fetch_stock(s, sem) for s in symbols]

    results = []
    completed = 0
    total = len(tasks)

    for coro in asyncio.as_completed(tasks):

        try:
            stock = await coro

            if stock and stock.get("avg_volume", 0) > 50000:
                results.append(stock)

        except:
            pass

        completed += 1

        if completed % 10 == 0:
            print(f"Progress {completed}/{total}")

    print(f"Loaded OK: {len(results)} | Failed: {total - len(results)}")

    return results
