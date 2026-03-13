from vnstock import Quote

def get_vnindex_data(days=20):

    try:

        # lấy dữ liệu VNINDEX
        quote = Quote(symbol="VNINDEX", source="VCI")

        df = quote.history(period="1y", interval="1D")

        # lấy N ngày gần nhất
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
