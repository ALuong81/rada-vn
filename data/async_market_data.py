import asyncio
import time
from vnstock import stock_historical_data
from .cache_layer import get_cache, set_cache


# ==============================
# CONFIG
# ==============================
MAX_CONCURRENT = 5
TIMEOUT = 6
RETRY = 1


# ==============================
# CORE FETCH (async wrapper)
# ==============================
async def fetch_stock(symbol, sem):

    if not symbol or len(symbol) != 3:
        return None

    cache = get_cache(symbol)
    if cache:
        return cache

    async with sem:

        for attempt in range(RETRY + 1):

            try:

                loop = asyncio.get_event_loop()

                start = time.time()

                df = await asyncio.wait_for(
                    loop.run_in_executor(
                        None,
                        lambda: stock_historical_data(
                            symbol=symbol,
                            start_date="2024-01-01",
                            end_date="2026-12-31",
                            resolution="1D"
                        )
                    ),
                    timeout=TIMEOUT
                )

                elapsed = round(time.time() - start, 2)

                if df is None or len(df) < 60:
                    return None

                close = df["close"]
                volume = df["volume"]

                data = {
                    "symbol": symbol,
                    "close": close.tolist(),
                    "volume": float(volume.iloc[-1]),
                    "avg_volume": float(volume.tail(20).mean()),
                    "price": round(float(close.iloc[-1]) / 1000, 2),
                    "resistance": round(float(close.tail(50).max()) / 1000, 2),
                }

                set_cache(symbol, data)

                return data

            except asyncio.TimeoutError:
                print(f"[TIMEOUT] {symbol}")

            except Exception as e:

                err = str(e).lower()

                if "invalid symbol" in err or "bad request" in err:
                    print(f"[INVALID] {symbol}")
                    return None

                print(f"[RETRY {attempt+1}] {symbol}")

            await asyncio.sleep(0.5)

    return None
