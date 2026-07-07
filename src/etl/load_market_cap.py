import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"
EXCEL_FILE = "data/raw/market_cap.xlsx"


def clean_columns(df):
    """
    Standardize Excel column names.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("%", "pct", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def create_table(conn):
    """
    Creates market_cap table if it doesn't already exist.
    """

    conn.execute("""
    CREATE TABLE IF NOT EXISTS market_cap (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,
        company_name TEXT,

        market_cap_cr REAL,
        enterprise_value_cr REAL,

        pe_ratio REAL,
        pb_ratio REAL,

        dividend_yield_pct REAL,

        face_value REAL,
        current_price REAL
    )
    """)

    conn.commit()


def main():

    print("=" * 60)
    print("LOADING MARKET CAP DATA")
    print("=" * 60)

    df = pd.read_excel(EXCEL_FILE)

    df = clean_columns(df)

    print("\nColumns found:")
    print(df.columns.tolist())

    rename_map = {

        "company_id": "company_id",
        "company_name": "company_name",

        "market_cap": "market_cap_cr",
        "market_cap_(cr)": "market_cap_cr",
        "market_cap_cr": "market_cap_cr",

        "enterprise_value": "enterprise_value_cr",
        "enterprise_value_(cr)": "enterprise_value_cr",
        "enterprise_value_cr": "enterprise_value_cr",

        "p/e": "pe_ratio",
        "pe": "pe_ratio",
        "pe_ratio": "pe_ratio",

        "p/b": "pb_ratio",
        "pb": "pb_ratio",
        "pb_ratio": "pb_ratio",

        "dividend_yield": "dividend_yield_pct",
        "dividend_yield_%": "dividend_yield_pct",
        "dividend_yield_pct": "dividend_yield_pct",

        "face_value": "face_value",
        "current_price": "current_price"

    }

    df.rename(columns=rename_map, inplace=True)

    required_columns = [

        "company_id",
        "company_name",
        "market_cap_cr",
        "enterprise_value_cr",
        "pe_ratio",
        "pb_ratio",
        "dividend_yield_pct",
        "face_value",
        "current_price"

    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    df = df[required_columns]

    conn = sqlite3.connect(DB_PATH)

    # Create table if missing
    create_table(conn)

    # Remove old rows
    conn.execute("DELETE FROM market_cap")
    conn.commit()

    # Insert new rows
    df.to_sql(
        "market_cap",
        conn,
        if_exists="append",
        index=False
    )

    print("\nRows inserted:", len(df))

    print("\nSample Data:\n")

    print(
        pd.read_sql(
            "SELECT * FROM market_cap LIMIT 5",
            conn
        )
    )

    conn.close()

    print("\nDone!")
    print("=" * 60)


if __name__ == "__main__":
    main()