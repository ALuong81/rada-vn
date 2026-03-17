from engine.scanner_engine import scan_market
from analysis.universe_v3 import build_universe_v3

# Market
from analysis.market_breadth_engine import analyze_market
from analysis.market_timing_engine import market_timing_engine
from analysis.vnindex_data_engine import get_vnindex_data
from analysis.vnindex_trend_engine import vnindex_trend

# Sector
from analysis.sector_rotation_engine import sector_rotation, detect_sector
from analysis.sector_rotation_pro import sector_rotation_pro
from analysis.sector_heatmap_engine import sector_heatmap

# Liquidity
from analysis.liquidity_ranking_engine import liquidity_ranking
from analysis.liquidity_engine import liquidity_signal

# Trend
from analysis.multi_timeframe_engine import scan_trend
from analysis.multi_tf_engine import multi_tf_trend

# Strength
from analysis.relative_strength_engine import relative_strength
from analysis.leader_stock_engine import detect_leaders

# Smart money
from analysis.smart_money_engine import scan_smart_money
from analysis.institutional_accumulation_engine import institutional_accumulation

# Volume + Risk
from analysis.volume_engine import scan_volume
from analysis.risk_filter_engine import scan_risk
from analysis.fake_breakout_filter import filter_fake_breakout

# Patterns
from analysis.vcp_detector import scan_vcp
from analysis.supply_dryup_detector import supply_dryup
from analysis.pattern_ai_engine import detect_pattern
from analysis.super_stock_detector import scan_super_stocks

# Breakout
from analysis.breakout_engine import breakout_status, breakout_probability
from analysis.super_breakout_engine import detect_super_breakout
from analysis.early_breakout_detector import early_breakout
from analysis.whale_order_detector import detect_whale_orders

# Scoring
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks

# Selection
from signals.sniper_selector import select_sniper
from signals.super_sniper_selector import super_sniper_selector

# Report
from report.telegram_report import send_report


def run():

    try:

        # =================================================
        # STEP 1: SCAN MARKET
        # =================================================
        print("\nSTEP 1: Scan market")

        stocks = scan_market()

        if not stocks:
            print("❌ No market data loaded")
            return

        print("Before universe filter:", len(stocks))

        stocks = build_universe_v3(stocks, top_n=80)

        print("After universe V3:", len(stocks))

        print("Loaded stocks:", len(stocks))

        # =================================================
        # BASE FILTER (LIQUIDITY)
        # =================================================
        stocks = [
            s for s in stocks
            if s.get("avg_volume", 0) > 50000
        ]

        print("After liquidity filter:", len(stocks))

        if not stocks:
            print("❌ All stocks filtered out")
            return

        # =================================================
        # STEP 2: DETECT SECTOR
        # =================================================
        print("\nSTEP 2: Detect sector")

        for s in stocks:
            symbol = s.get("symbol")
            if symbol:
                try:
                    s["sector"] = detect_sector(symbol)
                except:
                    s["sector"] = "UNKNOWN"

        # =================================================
        # STEP 3: LIQUIDITY RANKING
        # =================================================
        print("\nSTEP 3: Liquidity ranking")

        stocks = liquidity_ranking(stocks)

        print("After ranking:", len(stocks))

        # =================================================
        # STEP 4: MARKET ANALYSIS
        # =================================================
        print("\nSTEP 4: Market analysis")

        market = analyze_market(stocks)

        index_data = get_vnindex_data()

        if index_data:

            market_info = market_timing_engine(index_data)

            market["timing"] = market_info.get("timing", "UNKNOWN")
            market["distribution_days"] = market_info.get("distribution_days", 0)
            market["follow_through"] = market_info.get("follow_through", False)
            market["vnindex_trend"] = vnindex_trend(index_data)

        else:
            market["timing"] = "UNKNOWN"
            market["vnindex_trend"] = "UNKNOWN"

        print("Market timing:", market.get("timing"))

        # =================================================
        # STEP 5: SECTOR HEATMAP
        # =================================================
        print("\nSTEP 5: Sector heatmap")

        heatmap = sector_heatmap(stocks)
        strong_sectors, weak_sectors = sector_rotation_pro(stocks)

        print("Top sectors:", heatmap[:5])

        # =================================================
        # STEP 6: PIPELINE
        # =================================================
        print("\nSTEP 6: Analysis pipeline")

        stocks = sector_rotation(stocks)
        stocks = scan_trend(stocks)
        stocks = relative_strength(stocks)

        stocks = scan_vcp(stocks)
        stocks = scan_super_stocks(stocks)

        stocks = scan_smart_money(stocks)
        stocks = scan_volume(stocks)

        stocks = scan_risk(stocks)

        stocks = detect_leaders(stocks)
        stocks = filter_fake_breakout(stocks)

        # =================================================
        # STEP 7: STOCK LEVEL ANALYSIS
        # =================================================
        print("\nSTEP 7: Stock analysis")

        results = []

        for s in stocks:

            try:

                if "close" not in s or "volume" not in s:
                    continue

                s["trend"] = multi_tf_trend(s)
                s["pattern"] = detect_pattern(s)
                s["accumulation"] = supply_dryup(s)

                s["liquidity"] = liquidity_signal(s)
                s["institutional_flow"] = institutional_accumulation(s)

                s["breakout_prob"] = breakout_probability(s)
                s["super_breakout"] = detect_super_breakout(s)
                s["early_breakout"] = early_breakout(s)

                s["whale_flow"] = detect_whale_orders(s)

                s["meta_score"] = score_stock(s)

                s["leader"] = "YES" if s["meta_score"] > 70 else "NO"
                s["status"] = breakout_status(s)

                results.append(s)

            except Exception as e:
                print(f"[SKIP STOCK] {s.get('symbol')} → {e}")

        print("Stocks analyzed:", len(results))

        if not results:
            print("❌ No valid stocks after analysis")
            return

        # =================================================
        # STEP 8: RANKING
        # =================================================
        print("\nSTEP 8: Ranking")

        ranked = rank_stocks(results)

        # =================================================
        # STEP 9: SNIPER
        # =================================================
        print("\nSTEP 9: Sniper selection")

        sniper = select_sniper(ranked)
        super_sniper = super_sniper_selector(ranked)

        # =================================================
        # MARKET FILTER
        # =================================================
        timing = market.get("timing", "UNKNOWN")

        if timing == "MARKET IN CORRECTION":
            for s in sniper:
                s["status"] = "⛔ MARKET BAD"
            sniper = sniper[:1]

        elif timing == "MARKET UNDER PRESSURE":
            for s in sniper:
                s["status"] = "⚠ WATCH"
            sniper = sniper[:2]

        elif timing == "CONFIRMED UPTREND":
            sniper = sniper[:5]

        print("Final sniper:", len(sniper))

        # =================================================
        # STEP 10: REPORT
        # =================================================
        print("\nSTEP 10: Send report")

        send_report(
            sniper,
            market,
            heatmap,
            strong_sectors,
            weak_sectors
        )

        print("✅ RADA report sent")

    except Exception as e:

        import traceback

        print("❌ RADA SYSTEM ERROR:", e)
        traceback.print_exc()


if __name__ == "__main__":
    run()
