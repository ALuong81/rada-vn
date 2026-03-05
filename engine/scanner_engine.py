import pandas as pd

from core.vnstock_api import get_price
from indicators.momentum import momentum_score
from indicators.volume import volume_score
from indicators.breakout import breakout

from ai.leader_predictor import predict_leader

from engine.wyckoff_engine import detect_wyckoff
from engine.smartmoney_engine import liquidity_grab


def scan(symbol):

    df = get_price(symbol)

    if df is None:
        return None

    mom = momentum_score(df)
    vol = volume_score(df)

    if mom < 5:
        return None

    if vol < 1.2:
        return None

    if not breakout(df):
        return None

    prob = predict_leader(symbol)

    price = df.close.iloc[-1]

    entry = price * 1.01
    target = price * 1.15
    stop = price * 0.95

    return {
        "symbol": symbol,
        "price": price,
        "entry": entry,
        "target": target,
        "stop": stop,
        "prob": prob
    }
