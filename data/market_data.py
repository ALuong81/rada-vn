from vnstock import stock_historical_data
from .cache_layer import get_cache, set_cache

import contextlib
import io
import time
import random


def load_stock(symbol):

    # =========================
    # L1 + L2 CACHE
    # =========================
    cache = get_cache(symbol)
    if cache:
        return cache

    retries = 3

    for attempt in range(retries):

        try:

            with contextlib.redirect_stdout(io.StringIO()):

                df = stock_historical_data(
                    symbol=symbol,
                    start_date="2024-01-01",
                    end_date="2026-12-31",
                    resolution="1D"
                )

            if df is None or len(df) < 60:
                return None

            close = df["close"]
            volume = df["volume"]

            data = {
                "symbol": symbol,
                "close": close.tolist(),   # convert để cache được
                "volume": float(volume.iloc[-1]),
                "avg_volume": float(volume.tail(20).mean()),
                "price": float(close.iloc[-1]) / 1000,
                "resistance": float(close.tail(50).max()) / 1000,
            }

            set_cache(symbol, data)

            return data

        except Exception:

            wait = 1 + random.uniform(0, 2)
            print(f"[RETRY {attempt+1}] {symbol} ({round(wait,1)}s)")
            time.sleep(wait)

    # =========================
    # FALLBACK CACHE (hết hạn)
    # =========================
    print(f"[FALLBACK] {symbol}")

    old = get_cache(symbol)
    if old:
        return old

    return None
