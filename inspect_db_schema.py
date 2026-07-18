import sqlite3

conn = sqlite3.connect('db/nifty100.db')
cur = conn.cursor()
print(cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall())
for name in ['companies','financial_ratios','profitandloss','balancesheet','cashflow','sectors','prosandcons']:
    cols = cur.execute(f'PRAGMA table_info({name})').fetchall()
    print('\n' + name)
    for c in cols:
        print(c[1])
conn.close()
