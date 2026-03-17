from vnstock import listing_companies, stock_historical_data
from .cache_layer import get_cache, set_cache

import contextlib
import io
import time


# =========================================
# GET SYMBOLS (CLEAN VERSION)
# =========================================
def get_symbols():

    try:
        df = listing_companies()

        if df is None or len(df) == 0:
            return []

        # ✅ nếu có exchange → lọc HOSE + HNX
        if "exchange" in df.columns:
            df = df[df["exchange"].isin(["HOSE", "HNX"])]

        symbols = df["ticker"].dropna().tolist()

        clean = []

        for s in symbols:

            if not isinstance(s, str):
                continue

            s = s.strip().upper()

            # ✅ chỉ giữ mã chuẩn
            if not s.isalpha():
                continue

            if len(s) != 3:
                continue

            # ❌ blacklist cơ bản
            if s in ["ETF", "VNINDEX", "VN30"]:
                continue

            clean.append(s)

        # remove duplicate
        clean = list(set(clean))

        print("Universe loaded:", len(clean))

        return clean

    except Exception as e:
        print("Error loading symbols:", e)
        return []


# =========================================
# LOAD STOCK (STABLE VERSION)
# =========================================
def load_stock(symbol):

    # ❌ chặn từ đầu
    if not symbol or len(symbol) != 3:
        return None

    # cache
    cache = get_cache(symbol)
    if cache:
        return cache

    for attempt in range(2):

        try:
            start = time.time()

            # tắt log vnstock
            with contextlib.redirect_stdout(io.StringIO()):

                df = stock_historical_data(
                    symbol=symbol,
                    start_date="2024-01-01",
                    end_date="2026-12-31",
                    resolution="1D"
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

        except Exception as e:

            err = str(e).lower()

            # ❌ invalid symbol → bỏ luôn
            if "invalid symbol" in err or "bad request" in err:
                print(f"[INVALID] {symbol}")
                return None

            # retry nhẹ
            print(f"[RETRY {attempt+1}] {symbol}")

            time.sleep(1)

    return None
