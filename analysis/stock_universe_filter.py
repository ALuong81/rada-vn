from vnstock import listing_companies


def get_stock_universe():

    try:
        df = listing_companies()
    except Exception as e:
        print("Không tải được danh sách cổ phiếu:", e)
        return []

    if df is None or df.empty:
        print("Listing rỗng")
        return []

    # chuẩn hoá tên cột
    df.columns = [c.lower() for c in df.columns]

    # tìm cột symbol
    symbol_col = None

    for c in ["symbol", "ticker", "code"]:
        if c in df.columns:
            symbol_col = c
            break

    if symbol_col is None:
        print("Không tìm thấy cột symbol")
        print("Columns:", df.columns.tolist())
        return []

    symbols = df[symbol_col].dropna().unique().tolist()

    # loại mã không phải cổ phiếu
    symbols = [s for s in symbols if isinstance(s, str) and len(s) <= 3]

    print(f"Universe loaded: {len(symbols)} symbols")

    return symbols
