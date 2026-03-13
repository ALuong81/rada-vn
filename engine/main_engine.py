from data.market_data import get_symbols, load_stock

from engine.scanner_engine import scan_market

from analysis.sector_rotation_engine import sector_rotation
from analysis.multi_timeframe_engine import scan_trend
from analysis.volume_engine import scan_volume
from analysis.vcp_detector import scan_vcp
from analysis.leader_stock_engine import detect_leaders
from analysis.fake_breakout_filter import filter_fake_breakout
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks
from analysis.market_breadth_engine import market_breadth

from signals.sniper_selector import select_sniper

from report.telegram_report import send_report


def run():

    symbols = get_symbols()

    print("Loaded symbols:", len(symbols))

    stocks = []

    for sym in symbols:

        data = load_stock(sym)

        if data:
            stocks.append(data)

    print("Total stocks:", len(stocks))

    if len(stocks) == 0:
        print("No stock data loaded")
        return

    # =========================
    # ANALYSIS PIPELINE
    # =========================

    stocks = sector_rotation(stocks)

    stocks = scan_trend(stocks)

    stocks = scan_volume(stocks)

    stocks = scan_vcp(stocks)

    stocks = detect_leaders(stocks)

    stocks = filter_fake_breakout(stocks)

    # =========================
    # META SCORE
    # =========================

    for s in stocks:
        s["meta_score"] = score_stock(s)

    # =========================
    # AI RANKING
    # =========================

    ranked = rank_stocks(stocks)

    # =========================
    # SNIPER FILTER
    # =========================

    sniper = select_sniper(ranked)

    print("Sniper candidates:", len(sniper))

    # =========================
    # MARKET ANALYSIS
    # =========================

    market = market_breadth(stocks)

    # =========================
    # REPORT
    # =========================

    send_report(sniper, market)


if __name__ == "__main__":
    run()
