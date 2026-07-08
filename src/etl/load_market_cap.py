import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"
EXCEL_FILE = "data/raw/market_cap.xlsx"


def main():

    print("=" * 60)
    print("LOADING MARKET CAP DATA")
    print("=" * 60)

    df = pd.read_excel(EXCEL_FILE)

    print("\nRows in Excel :", len(df))

    print("\nColumns:")
    print(df.columns.tolist())

    conn = sqlite3.connect(DB_PATH)

    # Clear old data
    conn.execute("DELETE FROM market_cap")

    # Insert exactly the columns in the database
    df.to_sql(
        "market_cap",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    total = conn.execute(
        "SELECT COUNT(*) FROM market_cap"
    ).fetchone()[0]

    print("\nRows inserted :", total)

    print("\nSample Data")

    print(
        pd.read_sql(
            "SELECT * FROM market_cap LIMIT 5",
            conn
        )
    )

    conn.close()

    print("\nDone.")


if __name__ == "__main__":
    main()