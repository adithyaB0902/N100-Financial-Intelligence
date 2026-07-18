import sqlite3
import pandas as pd

conn = sqlite3.connect('db/nifty100.db')
print(pd.read_sql_query('SELECT * FROM financial_ratios WHERE company_id = "ABB" ORDER BY year DESC LIMIT 5', conn).to_string())
conn.close()
