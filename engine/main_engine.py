from analysis.market_cycle_engine import market_cycle
from analysis.institutional_engine import institutional_flow
from analysis.breakout_probability_engine import breakout_probability
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
from analysis.breakout_engine import breakout_status, breakout_probability

from engine.scanner_engine import scan_market

from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks

from signals.sniper_selector import select_sniper

from report.telegram_report import send_report

from analysis.market_breadth_engine import analyze_market
from analysis.multi_tf_engine import multi_tf_trend
from analysis.vcp_detector import scan_vcp
from analysis.supply_dryup_detector import supply_dryup


def run():

    # LOAD DATA
    stocks = scan_market()

    if not stocks:
        print("No market data loaded")
        return

    print("Total stocks:", len(stocks))

    # MARKET ANALYSIS
    market = analyze_market(stocks)

    # FILTER PIPELINE
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

    results = []

    for s in stocks:

        s["meta_score"] = score_stock(s)

        s["trend"] = multi_tf_trend(s)

        s["accumulation"] = supply_dryup(s)

        s["breakout_prob"] = breakout_probability(s)

        s["leader"] = "CÓ" if s["meta_score"] > 70 else "KHÔNG"

        s["sector"] = detect_sector(s["symbol"])
       
        s["cycle"] = market_cycle(s)
        
        s["institutional"] = institutional_flow(s)
        
        s["breakout_prob"] = breakout_probability(s)
       
        s["status"] = breakout_status(s)

        results.append(s)

    # RANK
    ranked = rank_stocks(results)

    # SNIPER
    sniper = select_sniper(ranked)

    # MARKET CONDITION FILTER

    if market.get("mode") == "DOWNTREND":

        for s in sniper:
            s["status"] = "THEO DOI - THI TRUONG XAU"

        sniper = sniper[:2]

    elif market.get("mode") == "SIDEWAY":

        for s in sniper:
            s["status"] = "THEO DOI TICH LUY"

    # SEND REPORT
    send_report(sniper, market)


if __name__ == "__main__":
    run()
