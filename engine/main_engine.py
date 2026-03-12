from engine.scanner_engine import scan_market
from analysis.meta_score import score_stock
from analysis.ai_ranking_engine import rank_stocks
from signals.sniper_selector import select_sniper
from report.telegram_report import send_report


def run():

    stocks = scan_market()

    if not stocks:
        print("No market data loaded")
        return

    results = []

    for s in stocks:

        s["meta_score"] = score_stock(s)

        results.append(s)

    ranked = rank_stocks(results)

    sniper = select_sniper(ranked)

    send_report(sniper)


if __name__ == "__main__":
    run()
