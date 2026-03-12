import os
import json
import time

CACHE_DIR = "cache"

def get_cache(symbol):

    path=f"{CACHE_DIR}/{symbol}.json"

    if not os.path.exists(path):
        return None

    with open(path) as f:
        data=json.load(f)

    if time.time()-data["time"]>3600:
        return None

    return data["data"]


def set_cache(symbol,data):

    os.makedirs(CACHE_DIR,exist_ok=True)

    path=f"{CACHE_DIR}/{symbol}.json"

    with open(path,"w") as f:

        json.dump({
            "time":time.time(),
            "data":data
        },f)
