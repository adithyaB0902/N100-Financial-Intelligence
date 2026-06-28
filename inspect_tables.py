import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "sectors"
]

for table in tables:
    print("\n" + "=" * 60)
    print(table.upper())

    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 2", conn)

    print(df.columns.tolist())

conn.close()