from analysis.sector_rotation_engine import sector_rotation
from analysis.market_breadth_engine import market_breadth
from analysis.breakout_engine import breakout_status
from engine.scanner_engine import scan_market
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks
from signals.sniper_selector import select_sniper
from report.telegram_report import send_report
from analysis.market_breadth_engine import market_breadth
from analysis.multi_tf_engine import multi_tf_trend
from analysis.smart_money_engine import smart_money
from analysis.vcp_detector import vcp_pattern
from analysis.supply_dryup_detector import supply_dryup
from analysis.breakout_engine import breakout_probability


def run():

    stocks = scan_market()
    stocks = sector_rotation(stocks)
    market = market_breadth(stocks)
 
    if not stocks:
        print("No market data loaded")
        return

    results = []

    for s in stocks:

        s["meta_score"] = score_stock(s)
        s["trend"] = multi_tf_trend(s)
        s["vcp"] = vcp_pattern(s)
        s["accumulation"] = supply_dryup(s)
        s["smart_money"] = smart_money(s)
        s["breakout_prob"] = breakout_probability(s)
        s["leader"] = "CÓ" if s["meta_score"] > 70 else "KHÔNG"
        s["sector"] = "UNKNOWN"
        s["status"] = breakout_status(s)
        
        results.append(s)

    ranked = rank_stocks(results)
    sniper = select_sniper(ranked)

    send_report(sniper, market)


if __name__ == "__main__":
    run()
