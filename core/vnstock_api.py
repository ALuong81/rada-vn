import pandas as pd
from vnstock import stock_historical_data

def get_price(symbol):

    df = stock_historical_data(
        symbol,
        "2024-01-01",
        "2026-12-31",
        resolution="1D"
    )

    return df
