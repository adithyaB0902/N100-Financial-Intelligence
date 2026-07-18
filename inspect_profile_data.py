import sqlite3
import pandas as pd

conn = sqlite3.connect('db/nifty100.db')
print(pd.read_sql_query('SELECT * FROM companies LIMIT 2', conn).to_string())
print('\nfinancial_ratios columns:', pd.read_sql_query('SELECT * FROM financial_ratios LIMIT 1', conn).columns.tolist())
print('\nprofitandloss columns:', pd.read_sql_query('SELECT * FROM profitandloss LIMIT 1', conn).columns.tolist())
print('\nsectors columns:', pd.read_sql_query('SELECT * FROM sectors LIMIT 1', conn).columns.tolist())
conn.close()
