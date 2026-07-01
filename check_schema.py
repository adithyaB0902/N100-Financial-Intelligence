import sqlite3
import os

print("Database:", os.path.abspath("db/nifty100.db"))
conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(financial_ratios);")

print("=" * 60)
print("FINANCIAL_RATIOS TABLE SCHEMA")
print("=" * 60)

for row in cursor.fetchall():
    print(row)

conn.close()