import asyncio

from engine.async_scanner_engine import scan_market_async
from analysis.universe_v3 import build_universe_v3

from analysis.liquidity_ranking_engine import liquidity_ranking
from analysis.liquidity_engine import liquidity_signal

from analysis.multi_tf_engine import multi_tf_trend
from analysis.pattern_ai_engine import detect_pattern
from analysis.supply_dryup_detector import supply_dryup

from analysis.institutional_accumulation_engine import institutional_accumulation
from analysis.breakout_engine import breakout_status, breakout_probability

from analysis.super_breakout_engine import detect_super_breakout
from analysis.early_breakout_detector import early_breakout
from analysis.whale_order_detector import detect_whale_orders

from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks

from signals.sniper_selector import select_sniper
from report.telegram_report import send_report


def run():

    try:

        print("STEP 1: Scan market")

        stocks = asyncio.run(scan_market_async())

        if not stocks:
            print("No data")
            return

        print("Before universe:", len(stocks))

        stocks = build_universe_v3(stocks)

        print("After universe:", len(stocks))

        stocks = [s for s in stocks if s.get("avg_volume", 0) > 100000]

        print("After liquidity:", len(stocks))

        stocks = liquidity_ranking(stocks)

        print("After ranking:", len(stocks))

        # =====================
        # STOCK ANALYSIS
        # =====================
        results = []

        for s in stocks:

            if not all(k in s for k in ["close", "volume"]):
                continue

            try:

                s["trend"] = multi_tf_trend(s)
                s["pattern"] = detect_pattern(s)
                s["accumulation"] = supply_dryup(s)

                s["liquidity"] = liquidity_signal(s)
                s["institutional"] = institutional_accumulation(s)

                s["breakout_prob"] = breakout_probability(s)

                s["super_breakout"] = detect_super_breakout(s)
                s["early_breakout"] = early_breakout(s)
                s["whale"] = detect_whale_orders(s)

                s["meta_score"] = score_stock(s)
                s["status"] = breakout_status(s)

                results.append(s)

            except Exception as e:
                print(f"[ERROR] {s.get('symbol')}: {e}")
                results.append(s)

        print("Analyzed:", len(results))

        if not results:
            results = stocks[:10]

        ranked = rank_stocks(results)

        if not ranked:
            ranked = results

        sniper = select_sniper(ranked)

        if not sniper:
            sniper = ranked[:3]

        send_report(sniper, {}, [], [], [])

        print("DONE")

    except Exception as e:

        import traceback
        print("SYSTEM ERROR:", e)
        traceback.print_exc()


if __name__ == "__main__":
    run()
