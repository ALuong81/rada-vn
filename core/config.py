import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

VNSTOCK_API_KEY = os.getenv("VNSTOCK_API_KEY")

SCAN_LIMIT = 1000
TIMEFRAME = "1D"

BASE_PATH = "data/full_symbols.csv"
SECTOR_PATH = "data/sector_map.csv"
