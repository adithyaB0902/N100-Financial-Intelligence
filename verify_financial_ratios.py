import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn
)

print("=" * 60)
print("ROW COUNT VERIFICATION")
print("=" * 60)

print(count)

if count.iloc[0]["total_rows"] >= 1100:
    print("\n✅ PASS : Row count satisfies Sprint requirement.")
else:
    print("\n❌ FAIL : Less than 1100 rows.")

conn.close()