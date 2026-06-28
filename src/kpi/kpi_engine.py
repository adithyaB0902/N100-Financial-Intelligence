import sqlite3
import pandas as pd
from src.kpi.profitability import *
from src.kpi.leverage import *
from src.kpi.efficiency import *
from src.kpi.cashflow import *

DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    print(
        "KPI Engine Initialized"
    )

    print(
        f"P&L rows: {len(pnl)}"
    )

    print(
        f"BS rows: {len(bs)}"
    )

    print(
        f"CF rows: {len(cf)}"
    )

    conn.close()


if __name__ == "__main__":
    main()
