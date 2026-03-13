from analysis.vnindex_data_engine import get_vnindex_data
from analysis.market_timing_model import market_timing
from analysis.early_breakout_detector import early_breakout
from analysis.whale_order_detector import detect_whale_orders
from engine.scanner_engine import scan_market

# Market
from analysis.market_breadth_engine import analyze_market
from analysis.vnindex_trend_engine import vnindex_trend

# Sector
from analysis.sector_rotation_engine import sector_rotation, detect_sector
from analysis.sector_rotation_pro import sector_rotation_pro
from analysis.sector_heatmap_engine import sector_heatmap

# Liquidity
from analysis.liquidity_ranking_engine import liquidity_ranking

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
    # 2 Gán sector sớm
    # -------------------------------------------------

    for s in stocks:
        s["sector"] = detect_sector(s["symbol"])

    # -------------------------------------------------
    # 3 Lọc thanh khoản
    # -------------------------------------------------

    stocks = liquidity_ranking(stocks)

    print("After liquidity filter:", len(stocks))

    # -------------------------------------------------
    # 4 Phân tích thị trường
    # -------------------------------------------------

    market = analyze_market(stocks)

    index_data = [
    {"close": 1240, "volume": 800000},
    {"close": 1245, "volume": 820000},
    {"close": 1250, "volume": 830000},
    {"close": 1260, "volume": 850000},
    {"close": 1270, "volume": 900000},
    ]

    #index_data = get_vnindex_data(20)
    print("VNINDEX DATA:", index_data[:5])
    
    if not index_data:
        market["timing"] = "UNKNOWN"
    else:
        market["timing"] = market_timing(index_data)

    # VNINDEX trend
    vnindex = next((s for s in stocks if s.get("symbol") == "VNINDEX"), None)
    if vnindex:
        market["vnindex_trend"] = vnindex_trend(vnindex)
    else:
        market["vnindex_trend"] = "UNKNOWN"
    
    # -------------------------------------------------
    # 5 Heatmap ngành
    # -------------------------------------------------

    heatmap = sector_heatmap(stocks)

    print("Top sector strength:", heatmap[:5])

    # Sector rotation nâng cao
    strong_sectors, weak_sectors = sector_rotation_pro(stocks)

    # -------------------------------------------------
    # 6 Pipeline phân tích
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
    # 7 Phân tích từng cổ phiếu
    # -------------------------------------------------

    results = []

    for s in stocks:

        # Trend đa khung
        s["trend"] = multi_tf_trend(s)

        # Pattern AI
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

        # Meta score
        s["meta_score"] = score_stock(s)

        # Leader flag
        s["leader"] = "CÓ" if s["meta_score"] > 70 else "KHÔNG"

        # Status
        s["status"] = breakout_status(s)

        s["early_breakout"] = early_breakout(s)

        s["whale_flow"] = detect_whale_orders(s)

        results.append(s)

    # -------------------------------------------------
    # 8 AI Ranking
    # -------------------------------------------------

    ranked = rank_stocks(results)

    # -------------------------------------------------
    # 9 Chọn SNIPER
    # -------------------------------------------------

    sniper = select_sniper(ranked)

    # -------------------------------------------------
    # 10 Điều chỉnh theo thị trường
    # -------------------------------------------------

    mode = market.get("mode")

    if mode == "DOWNTREND":

        for s in sniper:
            s["status"] = "THEO DÕI - THỊ TRƯỜNG XẤU"

        sniper = sniper[:2]

    elif mode == "SIDEWAY":

        for s in sniper:
            s["status"] = "THEO DÕI TÍCH LUỸ"

        sniper = sniper[:3]

    elif mode == "UPTREND":

        sniper = sniper[:5]

    timing = market.get("timing")

    if timing == "MARKET IN CORRECTION":

        for s in sniper:
            s["status"] = "⛔ KHÔNG MUA - THỊ TRƯỜNG XẤU"

        sniper = sniper[:1]

    elif timing == "MARKET UNDER PRESSURE":

        for s in sniper:
            s["status"] = "⚠️ THEO DÕI"

        sniper = sniper[:2]

    elif timing == "CONFIRMED UPTREND":

        sniper = sniper[:5]
    
    # -------------------------------------------------
    # 11 Report
    # -------------------------------------------------

    send_report(
        sniper,
        market,
        heatmap,
        strong_sectors,
        weak_sectors
    )


if __name__ == "__main__":
    run()
