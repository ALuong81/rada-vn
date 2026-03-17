from vnstock import listing_companies


def get_stock_universe():

    try:

        df = listing_companies()

        if df is None or len(df) == 0:
            return []

        symbols = df["ticker"].dropna().tolist()

        symbols = [
            s.strip().upper()
            for s in symbols
            if isinstance(s, str)
            and s.strip().isalpha()
            and 2 <= len(s.strip()) <= 3
        ]

        symbols = list(set(symbols))

        print("Universe loaded:", len(symbols))

        return symbols

    except Exception as e:

        print("Universe error:", e)
        return []
