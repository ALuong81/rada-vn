def momentum_score(df):

    r1 = df.close.pct_change(5).iloc[-1]
    r2 = df.close.pct_change(20).iloc[-1]

    return (r1*0.6 + r2*0.4) * 100
