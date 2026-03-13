from engine.scanner_engine import scan_market

from analysis.market_breadth_engine import analyze_market
from analysis.liquidity_ranking_engine import liquidity_ranking
from analysis.sector_rotation_engine import sector_rotation, detect_sector
from analysis.sector_heatmap_engine import sector_heatmap

from analysis.multi_timeframe_engine import scan_trend
from analysis.multi_tf_engine import multi_tf_trend

from analysis.relative_strength_engine import relative_strength
from analysis.smart_money_engine import scan_smart_money
from analysis.institutional_accumulation_engine import institutional_accumulation

from analysis.volume_engine import scan_volume
from analysis.risk_filter_engine import scan_risk
from analysis.fake_breakout_filter import filter_fake_breakout

from analysis.leader_stock_engine import detect_leaders
from analysis.super_stock_detector import scan_super_stocks

from analysis.vcp_detector import scan_vcp
from analysis.supply_dryup_detector import supply_dryup

from analysis.breakout_engine import breakout_status, breakout_probability

from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks

from signals.sniper_selector import select_sniper
from report.telegram_report import send_report


def run():

    # 1️⃣ Scan toàn bộ thị trường
    stocks = scan_market()

    if not stocks:
        print("No market data loaded")
        return

    print("Loaded symbols:", len(stocks))

    # 2️⃣ Lọc thanh khoản
    stocks = liquidity_ranking(stocks)

    # 3️⃣ Phân tích thị trường
    market = analyze_market(stocks)

    # 4️⃣ Heatmap ngành
    heatmap = sector_heatmap(stocks)

    print("Top ngành mạnh:", heatmap[:5])

    # 5️⃣ Pipeline phân tích
    stocks = sector_rotation(stocks)
    stocks = scan_trend(stocks)
    stocks = scan_vcp(stocks)
    stocks = scan_super_stocks(stocks)
    stocks = relative_strength(stocks)
    stocks = scan_smart_money(stocks)
    stocks = scan_risk(stocks)
    stocks = scan_volume(stocks)
    stocks = detect_leaders(stocks)
    stocks = filter_fake_breakout(stocks)

    results = []

    # 6️⃣ Phân tích từng cổ phiếu
    for s in stocks:

        s["meta_score"] = score_stock(s)

        s["trend"] = multi_tf_trend(s)

        s["vcp"] = scan_vcp(s)

        s["accumulation"] = supply_dryup(s)

        s["smart_money"] = scan_smart_money(s)

        s["institutional_flow"] = institutional_accumulation(s)

        s["breakout_prob"] = breakout_probability(s)

        s["leader"] = "CÓ" if s["meta_score"] > 70 else "KHÔNG"

        s["sector"] = detect_sector(s["symbol"])

        s["status"] = breakout_status(s)

        results.append(s)

    # 7️⃣ AI Ranking
    ranked = rank_stocks(results)

    # 8️⃣ Chọn sniper
    sniper = select_sniper(ranked)

    # 9️⃣ Điều chỉnh theo thị trường

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

    # 🔟 Gửi báo cáo
    send_report(sniper, market)


if __name__ == "__main__":
    run()
