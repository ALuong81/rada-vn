from concurrent.futures import ThreadPoolExecutor

from data.market_data import load_stock,get_symbols
from config import THREAD_WORKERS


def scan_market():

    symbols=get_symbols()

    stocks=[]

    def worker(symbol):

        try:
            s=load_stock(symbol)
            stocks.append(s)
        except:
            pass

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as exe:

        exe.map(worker,symbols)

    return stocks
