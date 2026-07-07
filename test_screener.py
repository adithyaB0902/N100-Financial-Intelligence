import sqlite3
import pandas as pd

from src.screener.engine import ScreenerEngine


DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    print(f"Loaded rows : {len(df)}")

    engine = ScreenerEngine(df)

    result = engine.apply_filters()

    print(f"Filtered rows : {len(result)}")

    print("\nTop 10 Results\n")

    print(
        result[
            [
                "company_id",
                "return_on_equity_pct",
                "debt_to_equity",
                "composite_quality_score"
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()