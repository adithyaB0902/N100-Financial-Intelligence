import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "db/nifty100.db"

HEADER1_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
}


def load_excel(file_path):
    filename = Path(file_path).name

    if filename in HEADER1_FILES:
        return pd.read_excel(file_path, header=1)

    return pd.read_excel(file_path)


def main():

    conn = sqlite3.connect(DB_PATH)

    data_folder = Path("data/raw")

    audit = []

    table_map = {
        "companies.xlsx": "companies",
        "profitandloss.xlsx": "profitandloss",
        "balancesheet.xlsx": "balancesheet",
        "cashflow.xlsx": "cashflow",
        "analysis.xlsx": "analysis",
        "documents.xlsx": "documents",
        "prosandcons.xlsx": "prosandcons",
        "sectors.xlsx": "sectors",
        "stock_prices.xlsx": "stock_prices",
        "financial_ratios.xlsx": "financial_ratios",
        "peer_groups.xlsx": "peer_groups"
    }

    for file_name, table_name in table_map.items():

        file_path = data_folder / file_name

        df = load_excel(file_path)

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        audit.append({
            "table_name": table_name,
            "rows_loaded": len(df)
        })

        print(
            f"Loaded {table_name}: {len(df)} rows"
        )

    Path("output").mkdir(
        exist_ok=True
    )

    pd.DataFrame(audit).to_csv(
        "output/load_audit.csv",
        index=False
    )

    conn.close()

    print(
        "\nLoad complete."
    )


if __name__ == "__main__":
    main()
    