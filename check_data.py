import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("Years in financial_ratios:")
print(pd.read_sql("""
SELECT DISTINCT year
FROM financial_ratios
ORDER BY year
""", conn))

print("\nFirst 5 rows:")
print(pd.read_sql("""
SELECT *
FROM financial_ratios
LIMIT 5
""", conn))

conn.close()
