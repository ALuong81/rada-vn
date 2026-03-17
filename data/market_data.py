from vnstock import stock_historical_data
from .cache_layer import get_cache, set_cache

import contextlib
import io
import time


def load_stock(symbol):

    # check cache
    cache = get_cache(symbol)
    if cache:
        return cache

    retries = 2

    for attempt in range(retries):

        try:

            # tắt log vnstock
            with contextlib.redirect_stdout(io.StringIO()):

                df = stock_historical_data(
                    symbol=symbol,
                    start_date="2024-01-01",
                    end_date="2026-12-31",
                    resolution="1D"
                )

            if df is None or len(df) < 60:
                print(f"[SKIP] {symbol} → no data")
                return None

            close = df["close"]
            volume = df["volume"]

            data = {
                "symbol": symbol,
                "close": close,
                "volume": float(volume.iloc[-1]),
                "avg_volume": float(volume.tail(20).mean()),
                "price": float(close.iloc[-1]) / 1000,
                "resistance": float(close.tail(50).max()) / 1000,
            }

            # save cache
            set_cache(symbol, data)

            return data

        except Exception as e:

            print(f"[RETRY {attempt+1}] {symbol}")

            time.sleep(1)

    print(f"[FAIL] {symbol}")
    return None
