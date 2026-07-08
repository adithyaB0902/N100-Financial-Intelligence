import sqlite3
import pandas as pd

from src.screener.engine import ScreenerEngine
from src.screener.presets import PRESETS

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

engine = ScreenerEngine(df)

print("=" * 70)
print("DAY 16 - PRESET TEST")
print("=" * 70)

for preset_name in PRESETS:

    result = engine.apply_preset(preset_name)

    print(f"\nPreset : {preset_name}")
    print(f"Companies : {len(result)}")

    cols = [
        c for c in [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct",
            "composite_quality_score"
        ]
        if c in result.columns
    ]

    print(result[cols].head())

print("\nFinished.")