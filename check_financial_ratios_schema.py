import sqlite3

DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "PRAGMA table_info(financial_ratios);"
    )

    columns = cursor.fetchall()

    print("=" * 60)
    print("FINANCIAL_RATIOS TABLE SCHEMA")
    print("=" * 60)

    for column in columns:
        print(column)

    print("\nTotal Columns:", len(columns))

    conn.close()


if __name__ == "__main__":
    main()