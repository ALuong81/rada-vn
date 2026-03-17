from vnstock import listing_companies, stock_historical_data
from .cache_layer import get_cache, set_cache

import contextlib
import io


# -------------------------------------------------
# Load danh sách ticker
# -------------------------------------------------

def get_symbols():

    try:

        df = listing_companies()

        if df is None or len(df) == 0:
            print("get_symbols df rỗng")
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

        print("Universe loaded:", len(symbols))

        return symbols

    except Exception as e:

        print("Error loading symbols:", e)
        return []


# -------------------------------------------------
# Load dữ liệu cổ phiếu
# -------------------------------------------------

def load_stock(symbol):

    # kiểm tra cache
    cache = get_cache(symbol)
    if cache:
        return cache

    df = None

    try:

        # tắt log vnstock
        with contextlib.redirect_stdout(io.StringIO()):

            df = stock_historical_data(
                symbol=symbol,
                start_date="2024-01-01",
                end_date="2026-12-31",
                resolution="1D"
            )

    except Exception as e:

        print(f"API error: {symbol} - {e}")
        return None

    # kiểm tra dữ liệu
    if df is None or df.empty or len(df) < 60:
        return None

    try:

        close = df["close"]
        volume = df["volume"]

        price = float(close.iloc[-1]) / 1000
        vol = float(volume.iloc[-1])
        avg_volume = float(volume.tail(20).mean())

        # -------------------------------------------------
        # LỌC THANH KHOẢN
        # -------------------------------------------------

        if avg_volume < 200000:
            return None

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

        # cache lại
        set_cache(symbol, data)

        return data

    except Exception as e:

        print(f"Data parse error: {symbol} - {e}")
        return None
