import sqlite3
import os
DB_PATH = "db/nifty100.db"
SQL_FILE = "sql/upgrade_financial_ratios.sql"
import os

print("Database:", os.path.abspath("db/nifty100.db"))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_script = f.read()

try:
    cursor.executescript(sql_script)
    conn.commit()
    print("Database upgraded successfully.")
except Exception as e:
    print("Error:", e)

conn.close()