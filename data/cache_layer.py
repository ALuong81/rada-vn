import os
import json
import time

CACHE_DIR = "cache"
TTL = 60 * 60 * 6  # 6 tiếng

memory_cache = {}

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def get_cache(symbol):

    # L1 cache (RAM)
    if symbol in memory_cache:
        return memory_cache[symbol]

    path = f"{CACHE_DIR}/{symbol}.json"

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r") as f:
            data = json.load(f)

        # check TTL
        if time.time() - data["ts"] > TTL:
            return None

        memory_cache[symbol] = data["data"]
        return data["data"]

    except:
        return None


def set_cache(symbol, data):

    memory_cache[symbol] = data

    path = f"{CACHE_DIR}/{symbol}.json"

    try:
        with open(path, "w") as f:
            json.dump({
                "ts": time.time(),
                "data": data
            }, f)
    except:
        pass
