from vnstock import stock_historical_data
from datetime import datetime, timedelta


def get_vnindex_data(days=30):

    try:

        end = datetime.today()
        start = end - timedelta(days=days*3)

        df = stock_historical_data(
            symbol="VNINDEX",
            start_date=start.strftime("%Y-%m-%d"),
            end_date=end.strftime("%Y-%m-%d"),
            resolution="1D",
            type="index"
        )

        if df is None or df.empty:
            print("VNINDEX data empty")
            return []

        df = df.tail(days)

        data = []

        for _, row in df.iterrows():

            data.append({
                "close": float(row["close"]),
                "volume": float(row["volume"])
            })

        return data

    except Exception as e:

        print("VNINDEX API ERROR:", e)
        return []
