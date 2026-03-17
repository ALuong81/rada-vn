def safe_float(val):

    # pandas Series → lấy giá trị cuối
    if hasattr(val, "iloc"):
        try:
            return float(val.iloc[-1])
        except:
            return 0

    try:
        return float(val)
    except:
        return 0


def rank_stocks(stocks):

    for s in stocks:

        raw_score = s.get("meta_score", 0)

        s["ai_score"] = safe_float(raw_score)

    ranked = sorted(
        stocks,
        key=lambda x: x.get("ai_score", 0),
        reverse=True
    )

    return ranked
