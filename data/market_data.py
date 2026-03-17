from vnstock import listing_companies

INVALID_CACHE = set()


def get_symbols():

    try:
        df = listing_companies()

        if df is None or len(df) == 0:
            return []

        if "exchange" in df.columns:
            df = df[df["exchange"].isin(["HOSE", "HNX"])]

        symbols = df["ticker"].dropna().tolist()

        clean = []

        for s in symbols:

            if not isinstance(s, str):
                continue

            s = s.strip().upper()

            if not s.isalpha():
                continue

            if len(s) != 3:
                continue

            # lọc rác phổ biến
            if s.startswith(("X", "Z")):
                continue

            clean.append(s)

        clean = list(set(clean))

        print("Universe loaded:", len(clean))

        return clean

    except Exception as e:
        print("Error loading symbols:", e)
        return []
