import sqlite3
import pandas as pd
from src.screener.ranking import top_n
from src.screener.screener import FinancialScreener

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

results = (
    FinancialScreener(df)
    .latest_year()
    .reasonable_roe()
    .high_roe(20)
    .low_debt(1)
    .positive_growth()
    .high_quality(70)
    .get_results()
)
print(f"Companies found: {len(results)}")

top = top_n(results, 10)
results.to_csv(
    "output/screener_results.csv",
    index=False
)

print("Results exported to output/screener_results.csv")

print(f"Companies found: {len(results)}")

top = top_n(results, 10)

print("\nTop 10 Companies\n")

print(
    top[
        [
            "company_id",
            "year",
            "composite_quality_score",
            "return_on_equity_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr"
        ]
    ]
)