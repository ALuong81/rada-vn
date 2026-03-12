from engine.scanner_engine import scan_market
from analysis.breakout_engine import breakout
from analysis.meta_score import meta_score
from analysis.fake_breakout_filter import fake_breakout_filter
from analysis.ai_ranking_engine import rank_stocks
from signals.sniper_selector import sniper
from report.telegram_report import send_report


def run():

    stocks=scan_market()

    results=[]
    if len(results)==0:
        stocks = sorted(stocks, key=lambda x: x["change"], reverse=True)
        results = stocks[:3]
    for s in stocks:

        status,prob=breakout(s)

        s["status"]=status
        s["prob"]=prob

        if fake_breakout_filter(s):
            continue

        s["meta_score"]=meta_score(s)

        if sniper(s):

            results.append(s)

    ranked=rank_stocks(results)

    send_report(ranked[:3])

    print("Total stocks:", len(stocks))
    print("Sniper candidates:", len(results))
if __name__=="__main__":
    run()
