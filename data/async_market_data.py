import asyncio
from vnstock import stock_historical_data
from .market_data import INVALID_CACHE

MAX_CONCURRENT = 4
TIMEOUT = 6


async def fetch_stock(symbol, sem):

    if not symbol or len(symbol) != 3:
        return None

    if symbol in INVALID_CACHE:
        return None

    async with sem:

        try:
            loop = asyncio.get_event_loop()

            df = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: stock_historical_data(
                        symbol=symbol,
                        start_date="2024-01-01",
                        end_date="2026-12-31",
                        resolution="1D"
                    )
                ),
                timeout=TIMEOUT
            )

            if df is None or len(df) < 60:
                return None

            close = df["close"]
            volume = df["volume"]

            # 🔥 FIX QUAN TRỌNG: giữ pandas
            data = {
                "symbol": symbol,
                "close": close,
                "volume": volume,
                "avg_volume": float(volume.tail(20).mean()),
                "price": float(close.iloc[-1]),
                "resistance": float(close.tail(50).max()),
            }

            return data

        except asyncio.TimeoutError:
            return None

        except Exception as e:

            err = str(e).lower()

            if "invalid symbol" in err or "bad request" in err:
                INVALID_CACHE.add(symbol)
                return None

            return None
