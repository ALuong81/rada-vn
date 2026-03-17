import asyncio

# =========================
# CORE
# =========================
from engine.async_scanner_engine import scan_market_async
from analysis.universe_v3 import build_universe_v3

# Liquidity
from analysis.liquidity_ranking_engine import liquidity_ranking
from analysis.liquidity_engine import liquidity_signal

# Trend + Pattern
from analysis.multi_tf_engine import multi_tf_trend
from analysis.pattern_ai_engine import detect_pattern
from analysis.supply_dryup_detector import supply_dryup

# Smart money
from analysis.institutional_accumulation_engine import institutional_accumulation

# Breakout
from analysis.breakout_engine import breakout_status, breakout_probability
from analysis.super_breakout_engine import detect_super_breakout
from analysis.early_breakout_detector import early_breakout
from analysis.whale_order_detector import detect_whale_orders

# Score + Rank
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks

# Selection
from signals.sniper_selector import select_sniper

# Report
from report.telegram_report import send_report


# =========================
# MAIN
# =========================
def run():

    try:

        # =====================================
        # STEP 1: SCAN MARKET
        # =====================================
        print("STEP 1: Scan market")

        stocks = asyncio.run(scan_market_async())

        if not stocks:
            print("❌ No market data")
            return

        print("Before universe:", len(stocks))

        # =====================================
        # UNIVERSE FILTER
        # =====================================
        stocks = build_universe_v3(stocks)

        print("After universe:", len(stocks))

        if not stocks:
            print("⚠ fallback universe")
            stocks = stocks[:10]

        # =====================================
        # LIQUIDITY FILTER
        # =====================================
        stocks = [s for s in stocks if s.get("avg_volume", 0) > 100000]

        print("After liquidity:", len(stocks))

        if not stocks:
            print("⚠ fallback liquidity")
            stocks = stocks[:10]

        # =====================================
        # LIQUIDITY RANK
        # =====================================
        stocks = liquidity_ranking(stocks)

        print("After ranking:", len(stocks))

        if not stocks:
            print("❌ ranking failed")
            return

        # =====================================
        # STEP 2: STOCK ANALYSIS
        # =====================================
        print("STEP 2: Stock analysis")

        results = []

        for s in stocks:

            if not all(k in s for k in ["close", "volume"]):
                continue

            try:

                # ===== CORE ANALYSIS =====
                s["trend"] = multi_tf_trend(s)
                s["pattern"] = detect_pattern(s)
                s["accumulation"] = supply_dryup(s)

                # ===== FLOW =====
                s["liquidity"] = liquidity_signal(s)
                s["institutional"] = institutional_accumulation(s)

                # ===== BREAKOUT =====
                s["breakout_prob"] = breakout_probability(s)
                s["super_breakout"] = detect_super_breakout(s)
                s["early_breakout"] = early_breakout(s)
                s["whale"] = detect_whale_orders(s)

                # ===== SCORE (QUAN TRỌNG) =====
                s["meta_score"] = score_stock(s)

                # ===== STATUS =====
                s["status"] = breakout_status(s)

                results.append(s)

            except Exception as e:
                print(f"[ERROR] {s.get('symbol')}: {e}")
                results.append(s)  # 🔥 không drop

        print("Analyzed:", len(results))

        if not results:
            print("⚠ fallback results")
            results = stocks[:10]

        # =====================================
        # FIX SCALAR SCORE (CHỐNG SERIES)
        # =====================================
        for s in results:

            val = s.get("meta_score", 0)

            if hasattr(val, "iloc"):
                try:
                    val = float(val.iloc[-1])
                except:
                    val = 0

            try:
                s["meta_score"] = float(val)
            except:
                s["meta_score"] = 0

        # =====================================
        # STEP 3: RANKING
        # =====================================
        print("STEP 3: Ranking")

        ranked = rank_stocks(results)

        if not ranked:
            print("⚠ fallback ranking")
            ranked = results

        # =====================================
        # STEP 4: SNIPER
        # =====================================
        print("STEP 4: Sniper selection")

        sniper = select_sniper(ranked)

        if not sniper:
            print("⚠ fallback sniper")
            sniper = ranked[:3]

        # =====================================
        # STEP 5: REPORT
        # =====================================
        print("STEP 5: Send report")

        send_report(sniper, {}, [], [], [])

        print("✅ DONE - SYSTEM STABLE")

    except Exception as e:

        import traceback

        print("❌ SYSTEM ERROR:", e)
        traceback.print_exc()


# =========================
# RUN
# =========================
if __name__ == "__main__":
    run()
