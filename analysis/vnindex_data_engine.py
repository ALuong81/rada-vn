from vnstock import stock_historical_data


def get_vnindex_data(days=10):

    try:

        df = stock_historical_data(
            symbol="VNINDEX",
            start_date="2024-01-01",
            end_date=None,
            resolution="1D",
            type="index"
        )

        df = df.tail(days)

        data = []

        for _, row in df.iterrows():

            data.append({
                "close": float(row["close"]),
                "volume": float(row["volume"])
            })

        return data

    except Exception as e:

        print("VNINDEX API error:", e)

        return []
