import sqlite3
import pandas as pd

from src.screener.engine import ScreenerEngine

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

engine = ScreenerEngine(df)

result = engine.apply_preset("quality_compounder")

print("Companies:", result["company_id"].nunique())

print(
    result[
        [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
        ]
    ].head(10)
)
