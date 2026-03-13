from analysis.sector_rotation_pro import sector_rotation_pro
from engine.scanner_engine import scan_market
from analysis.super_stock_detector import scan_super_stocks

# Market
from analysis.market_breadth_engine import analyze_market
from analysis.vnindex_trend_engine import vnindex_trend

# Filters
from analysis.liquidity_ranking_engine import liquidity_ranking
from analysis.sector_rotation_engine import sector_rotation, detect_sector
from analysis.sector_heatmap_engine import sector_heatmap

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

# Breakout
from analysis.breakout_engine import breakout_status, breakout_probability
from analysis.super_breakout_engine import super_breakout

# Scoring
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks

# Selection
from signals.sniper_selector import select_sniper

# Report
from report.telegram_report import send_report


def run():

    # -------------------------------------------------
    # 1 Scan thị trường
    # -------------------------------------------------

    stocks = scan_market()

    if not stocks:
        print("No market data loaded")
        return

    print("Loaded symbols:", len(stocks))

    # -------------------------------------------------
    # 2 Lọc thanh khoản
    # -------------------------------------------------

    stocks = liquidity_ranking(stocks)

    print("After liquidity filter:", len(stocks))

    # -------------------------------------------------
    # 3 Phân tích thị trường
    # -------------------------------------------------

    market = analyze_market(stocks)

    # -------------------------------------------------
    # 4 Heatmap ngành
    # -------------------------------------------------

    heatmap = sector_heatmap(stocks)

    print("Top sector strength:", heatmap[:5])

    # sector rotation nâng cao
    strong_sectors, weak_sectors = sector_rotation_pro(stocks)

    # -------------------------------------------------
    # 5 Pipeline phân tích
    # -------------------------------------------------

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

    # -------------------------------------------------
    # 6 Phân tích từng cổ phiếu
    # -------------------------------------------------

    results = []

    for s in stocks:

        # Sector
        s["sector"] = detect_sector(s["symbol"])

        # Trend
        s["trend"] = multi_tf_trend(s)

        # Pattern
        s["pattern"] = detect_pattern(s)

        # VCP
        s["vcp"] = scan_vcp(s)

        # Accumulation
        s["accumulation"] = supply_dryup(s)

        # Smart money
        s["smart_money"] = scan_smart_money(s)

        # Institutional flow
        s["institutional_flow"] = institutional_accumulation(s)

        # Breakout probability
        s["breakout_prob"] = breakout_probability(s)

        # Super breakout
        s["super_breakout"] = super_breakout(s)

        # Score
        s["meta_score"] = score_stock(s)

        # Leader flag
        s["leader"] = "CÓ" if s["meta_score"] > 70 else "KHÔNG"

        # Status
        s["status"] = breakout_status(s)

        results.append(s)

    # -------------------------------------------------
    # 7 AI Ranking
    # -------------------------------------------------

    ranked = rank_stocks(results)

    # -------------------------------------------------
    # 8 Chọn SNIPER
    # -------------------------------------------------

    sniper = select_sniper(ranked)

    # -------------------------------------------------
    # 9 Điều chỉnh theo thị trường
    # -------------------------------------------------

    if market.get("mode") == "DOWNTREND":

        for s in sniper:
            s["status"] = "THEO DÕI - THỊ TRƯỜNG XẤU"

        sniper = sniper[:2]

    elif market.get("mode") == "SIDEWAY":

        for s in sniper:
            s["status"] = "THEO DÕI TÍCH LUỸ"

        sniper = sniper[:3]

    elif market.get("mode") == "UPTREND":

        sniper = sniper[:5]

    # -------------------------------------------------
    # 10 Report
    # -------------------------------------------------

    #send_report(sniper, market)
    send_report(sniper, market, heatmap, strong_sectors, weak_sectors)
    #sendr_report(sniper, market, heatmap)

if __name__ == "__main__":
    run()
