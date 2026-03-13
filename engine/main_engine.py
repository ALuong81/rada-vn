from analysis.relative_strength_engine import relative_strength
from analysis.smart_money_engine import scan_smart_money
from analysis.risk_filter_engine import scan_risk
from analysis.super_stock_detector import scan_super_stocks
from analysis.liquidity_filter import liquidity_filter
from analysis.multi_timeframe_engine import scan_trend
from analysis.leader_stock_engine import detect_leaders
from analysis.volume_engine import scan_volume
from analysis.fake_breakout_filter import filter_fake_breakout
from analysis.sector_rotation_engine import sector_rotation, detect_sector
from analysis.breakout_engine import breakout_status
from engine.scanner_engine import scan_market
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks
from signals.sniper_selector import select_sniper
from report.telegram_report import send_report
from analysis.market_breadth_engine import analyze_market
from analysis.multi_tf_engine import multi_tf_trend
from analysis.vcp_detector import scan_vcp
from analysis.supply_dryup_detector import supply_dryup
from analysis.breakout_engine import breakout_probability


def run():

    stocks = scan_market()
    market = analyze_market(stocks)
    if market.get("mode") == "DOWNTREND":
        for s in stocks:
            s["status"] = "THEO DÕI - THỊ TRƯỜNG XẤU"
    stocks = liquidity_filter(stocks)
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
 
    if not stocks:
        print("No market data loaded")
        return

    results = []

    for s in stocks:

        s["meta_score"] = score_stock(s)
        s["trend"] = multi_tf_trend(s)
        s["vcp"] = scan_vcp(s)
        s["accumulation"] = supply_dryup(s)
        s["smart_money"] = scan_smart_money(s)
        s["breakout_prob"] = breakout_probability(s)
        s["leader"] = "CÓ" if s["meta_score"] > 70 else "KHÔNG"
        s["sector"] = detect_sector(s["symbol"])
        s["status"] = breakout_status(s)
        
        results.append(s)

    ranked = rank_stocks(results)
    sniper = select_sniper(ranked)
    if market.get("mode") == "DOWNTREND":
        sniper = sniper[:2]
    
    send_report(sniper, market)


if __name__ == "__main__":
    run()
