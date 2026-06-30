import sqlite3
import pandas as pd
import os

from src.analytics.cashflow_kpis import (
    cfo_quality_score,
    capital_allocation_pattern
)

DB = "db/nifty100.db"
OUTPUT = "output/capital_allocation.csv"


def main():

    conn = sqlite3.connect(DB)

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    pnl = pd.read_sql(
        "SELECT company_id, year, net_profit FROM profitandloss",
        conn
    )

    conn.close()

    merged = cashflow.merge(
        pnl,
        on=["company_id", "year"],
        how="left"
    )

    rows = []

    for company_id, group in merged.groupby("company_id"):

        quality = cfo_quality_score(
            group["operating_activity"].tolist(),
            group["net_profit"].fillna(0).tolist()
        )

        for _, row in group.iterrows():

            label = capital_allocation_pattern(
                row["operating_activity"],
                row["investing_activity"],
                row["financing_activity"],
                quality
            )

            rows.append({
                "company_id": row["company_id"],
                "year": row["year"],
                "cfo_sign":
                    "+" if row["operating_activity"] >= 0 else "-",
                "cfi_sign":
                    "+" if row["investing_activity"] >= 0 else "-",
                "cff_sign":
                    "+" if row["financing_activity"] >= 0 else "-",
                "pattern_label": label
            })

    os.makedirs("output", exist_ok=True)

    pd.DataFrame(rows).to_csv(
        OUTPUT,
        index=False
    )

    print("=" * 45)
    print("Capital Allocation CSV Generated")
    print("=" * 45)
    print(f"Rows : {len(rows)}")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()