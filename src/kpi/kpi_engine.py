import sqlite3
import pandas as pd

from src.kpi.profitability import *
from src.kpi.leverage import *
from src.kpi.efficiency import *
from src.kpi.cashflow import *

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)

DB_PATH = "db/nifty100.db"


def calculate_company_cagr(pnl_df):
    """
    Calculate all CAGR metrics for one company.
    """

    pnl_df = pnl_df.sort_values("year")

    revenue_3, revenue_3_flag = revenue_cagr(pnl_df, 3)
    revenue_5, revenue_5_flag = revenue_cagr(pnl_df, 5)
    revenue_10, revenue_10_flag = revenue_cagr(pnl_df, 10)

    pat_3, pat_3_flag = pat_cagr(pnl_df, 3)
    pat_5, pat_5_flag = pat_cagr(pnl_df, 5)
    pat_10, pat_10_flag = pat_cagr(pnl_df, 10)

    eps_3, eps_3_flag = eps_cagr(pnl_df, 3)
    eps_5, eps_5_flag = eps_cagr(pnl_df, 5)
    eps_10, eps_10_flag = eps_cagr(pnl_df, 10)

    return {
        "revenue_cagr_3yr": revenue_3,
        "revenue_cagr_5yr": revenue_5,
        "revenue_cagr_10yr": revenue_10,

        "pat_cagr_3yr": pat_3,
        "pat_cagr_5yr": pat_5,
        "pat_cagr_10yr": pat_10,

        "eps_cagr_3yr": eps_3,
        "eps_cagr_5yr": eps_5,
        "eps_cagr_10yr": eps_10,

        "revenue_cagr_3yr_flag": revenue_3_flag,
        "revenue_cagr_5yr_flag": revenue_5_flag,
        "revenue_cagr_10yr_flag": revenue_10_flag,

        "pat_cagr_3yr_flag": pat_3_flag,
        "pat_cagr_5yr_flag": pat_5_flag,
        "pat_cagr_10yr_flag": pat_10_flag,

        "eps_cagr_3yr_flag": eps_3_flag,
        "eps_cagr_5yr_flag": eps_5_flag,
        "eps_cagr_10yr_flag": eps_10_flag,
    }


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

    print("====================================")
    print("KPI ENGINE INITIALIZED")
    print("====================================")

    print(f"P&L rows : {len(pnl)}")
    print(f"BS rows  : {len(bs)}")
    print(f"CF rows  : {len(cf)}")

    # -------------------------------
    # CAGR Demo
    # -------------------------------

    first_company = pnl["company_id"].iloc[0]

    company_data = pnl[
        pnl["company_id"] == first_company
    ]

    result = calculate_company_cagr(company_data)

    print("\n====================================")
    print(f"CAGR RESULTS : {first_company}")
    print("====================================")

    for key, value in result.items():
        print(f"{key:30} : {value}")

    conn.close()


if __name__ == "__main__":
    main()