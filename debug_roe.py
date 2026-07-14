import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

for company in ["INDIGO", "BEL"]:
    print("\n" + "=" * 60)
    print(company)
    print("=" * 60)

    query = f"""
    SELECT
        p.company_id,
        p.year,
        p.net_profit,
        b.equity_capital,
        b.reserves
    FROM profitandloss p
    JOIN balancesheet b
      ON p.company_id = b.company_id
     AND p.year = b.year
    WHERE p.company_id = '{company}'
    ORDER BY p.year DESC
    """

    df = pd.read_sql(query, conn)

    df["shareholders_equity"] = (
        df["equity_capital"] +
        df["reserves"]
    )

    print(df)

conn.close()