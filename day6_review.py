import sqlite3
import pandas as pd
conn = sqlite3.connect("db/nifty100.db")
print("=" * 60)
print("DAY 6 DATA QUALITY REVIEW")
print("=" * 60)
tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "financial_ratios",
    "peer_groups"
]
print("\nROW COUNTS")
for table in tables:
    count = pd.read_sql_query(
        f"SELECT COUNT(*) AS cnt FROM {table}",
        conn
    )["cnt"][0]

    print(f"{table:20} {count}")
print("\n\n5 RANDOM COMPANIES")
companies = pd.read_sql_query(
    """
    SELECT company_name
    FROM companies
    ORDER BY RANDOM()
    LIMIT 5
    """,
    conn
)
print(companies)
print("\n\nYEAR COVERAGE")
coverage = pd.read_sql_query(
    """
    SELECT
        company_id,
        COUNT(DISTINCT year) AS years_available
    FROM profitandloss
    GROUP BY company_id
    ORDER BY years_available
    """,
    conn
)
print(coverage.head(20))
print("\n\nCOMPANIES WITH <5 YEARS DATA")
few_years = coverage[
    coverage["years_available"] < 5
]
print(few_years)
print("\n\nFOREIGN KEY CHECK")
cursor = conn.cursor()
cursor.execute(
    "PRAGMA foreign_key_check;"
)
fk_errors = cursor.fetchall()
print(fk_errors)
conn.close()
print("\nReview Complete.")