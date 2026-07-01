import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print("=" * 70)
print("DAY 12 COLUMN VALIDATION")
print("=" * 70)

for column in df.columns:

    if column == "id":
        continue

    nulls = df[column].isna().sum()
    non_nulls = len(df) - nulls

    status = "PASS" if non_nulls > 0 else "FAIL"

    print(
        f"{column:<35}"
        f" Non-Null = {non_nulls:<5}"
        f" Null = {nulls:<5}"
        f"{status}"
    )

print("\nValidation Complete")