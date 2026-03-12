from config import SNIPER_SCORE

def sniper(stock):

    return stock["meta_score"] >= SNIPER_SCORE
