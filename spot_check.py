import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

companies = [
    "ABB",
    "TCS",
    "INFY"
]

for company in companies:

    print("=" * 70)

    print(company)

    print("=" * 70)

    df = pd.read_sql(
        f"""
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            revenue_cagr_5yr,
            composite_quality_score
        FROM financial_ratios
        WHERE company_id='{company}'
        ORDER BY year DESC
        LIMIT 5
        """,
        conn
    )

    print(df)

conn.close()