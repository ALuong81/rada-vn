import sqlite3

conn = sqlite3.connect("rada.db")

def save_signal(symbol, entry, target, stop, prob):

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS signals(
    symbol TEXT,
    entry REAL,
    target REAL,
    stop REAL,
    prob REAL
    )
    """)

    cur.execute(
        "INSERT INTO signals VALUES (?,?,?,?,?)",
        (symbol, entry, target, stop, prob)
    )

    conn.commit()
