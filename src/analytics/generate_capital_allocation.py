import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import (
    cfo_quality_score,
    capital_allocation_pattern
)

DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    # Load Cash Flow data
    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    # Load Net Profit from Profit & Loss table
    pnl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            net_profit
        FROM profitandloss
        """,
        conn
    )

    conn.close()

    # Merge Cash Flow with Net Profit
    df = cashflow.merge(
        pnl,
        on=["company_id", "year"],
        how="left"
    )

    rows = []

    for company in df["company_id"].unique():

        company_df = (
            df[df["company_id"] == company]
            .sort_values("year")
        )

        quality = cfo_quality_score(
            company_df["operating_activity"].tolist(),
            company_df["net_profit"].tolist()
        )

        for _, row in company_df.iterrows():

            pattern = capital_allocation_pattern(
                row["operating_activity"],
                row["investing_activity"],
                row["financing_activity"],
                quality
            )

            rows.append({
                "company_id": row["company_id"],
                "year": row["year"],
                "cfo_sign": "+" if row["operating_activity"] >= 0 else "-",
                "cfi_sign": "+" if row["investing_activity"] >= 0 else "-",
                "cff_sign": "+" if row["financing_activity"] >= 0 else "-",
                "pattern_label": pattern or "Unknown"
            })

    output = pd.DataFrame(rows)

    output.to_csv(
        "output/capital_allocation.csv",
        index=False
    )

    print("\nCapital Allocation Preview\n")
    print(output.head())

    print(f"\nRows exported: {len(output)}")
    print("\nCSV saved to: output/capital_allocation.csv")


if __name__ == "__main__":
    main()