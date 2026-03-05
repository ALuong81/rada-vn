import pandas as pd

from engine.scanner_engine import scan
from alerts.telegram_bot import send
from alerts.formatter import format_signal

symbols = pd.read_csv("data/full_symbols.csv")

for s in symbols.symbol:

    result = scan(s)

    if result:

        msg = format_signal(
            result["symbol"],
            result["price"],
            result["entry"],
            result["target"],
            result["stop"],
            result["prob"]
        )

        send(msg)
