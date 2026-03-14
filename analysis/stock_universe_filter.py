import pandas as pd
from vnstock import stock_screener


MIN_PRICE = 5
MIN_VOLUME = 300000
MIN_MARKETCAP = 500_000_000_000  # 500B


def get_stock_universe():

    try:

        df = stock_screener()

    except Exception as e:

        print("Không tải được danh sách cổ phiếu:", e)
        return []


    # chuẩn hóa tên cột nếu khác
    df.columns = [c.lower() for c in df.columns]


    # lọc dữ liệu thiếu
    df = df.dropna(subset=["symbol"])


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
