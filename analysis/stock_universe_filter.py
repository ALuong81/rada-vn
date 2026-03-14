import pandas as pd
from vnstock import listing_companies


MIN_PRICE = 5
MIN_VOLUME = 300000
MIN_MARKETCAP = 500_000_000_000  # 500B


def get_stock_universe():

    try:
        df = listing_companies()
    except Exception as e:
        print("Không tải được danh sách cổ phiếu:", e)
        return []

    if df is None or df.empty:
        print("Không có dữ liệu listing")
        return []

    # chuẩn hoá
    df.columns = [c.lower() for c in df.columns]

    # chỉ lấy cổ phiếu
    if "type" in df.columns:
        df = df[df["type"] == "stock"]

    # chỉ lấy sàn chính
    if "exchange" in df.columns:
        df = df[df["exchange"].isin(["HOSE", "HNX", "UPCOM"])]

    symbols = df["symbol"].dropna().unique().tolist()

    print(f"Loaded symbols: {len(symbols)}")

    # lọc điều kiện
    if "price" in df.columns:
        df = df[df["price"] >= MIN_PRICE]

    if "volume" in df.columns:
        df = df[df["volume"] >= MIN_VOLUME]

    if "marketcap" in df.columns:
        df = df[df["marketcap"] >= MIN_MARKETCAP]


    symbols = df["symbol"].unique().tolist()

    print(f"Universe filtered: {len(symbols)} symbols")

    return symbols
