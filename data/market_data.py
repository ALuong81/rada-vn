from vnstock import listing_companies, stock_historical_data
from .cache_layer import get_cache, set_cache

import contextlib
import io


def get_symbols():

    try:

        df = listing_companies()

        if df is None or len(df) == 0:
            return []

        symbols = df["ticker"].dropna().tolist()

        # lọc ticker hợp lệ
        symbols = [
            s.strip().upper()
            for s in symbols
            if isinstance(s, str)
            and s.strip().isalpha()
            and 2 <= len(s.strip()) <= 3
        ]

        # loại trùng
        symbols = list(set(symbols))

        return symbols

    except Exception as e:

        print("Error loading symbols:", e)

        return []


def load_stock(symbol):

    # kiểm tra cache trước
    cache = get_cache(symbol)
    if cache:
        return cache

    try:

        # tắt log từ vnstock (tránh spam invalid symbol)
        with contextlib.redirect_stdout(io.StringIO()):

            df = stock_historical_data(
                symbol=symbol,
                start_date="2024-01-01",
                end_date="2026-12-31",
                resolution="1D"
            )

    except Exception:
        return None

    if df is None or len(df) < 60:
        return None

    try:

        close = df["close"]
        volume = df["volume"]

        price = float(close.iloc[-1]) / 1000
        vol = float(volume.iloc[-1])
        avg_volume = float(volume.tail(20).mean())

        resistance = float(close.tail(50).max()) / 1000

        change = float(close.pct_change().iloc[-1] * 100)

        data = {
            "symbol": symbol,
            "price": round(price, 2),
            "volume": vol,
            "avg_volume": avg_volume,
            "resistance": round(resistance, 2),
            "change": round(change, 2)
        }

        # lưu cache
        set_cache(symbol, data)

        return data

    except Exception:
        return None
