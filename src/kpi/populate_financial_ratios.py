import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

from src.analytics.cashflow_kpis import (
    free_cash_flow
)
from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr
)

from src.analytics.quality_score import (
    composite_quality_score
)
from src.analytics.validator import FinancialValidator
from src.analytics.anomaly_detector import AnomalyDetector
from src.analytics.report_generator import ValidationReport

DB_PATH = "db/nifty100.db"


def load_data():
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

    conn.close()

    merged = (
        pnl.merge(
            bs,
            on=["company_id", "year"],
            how="inner"
        )
        .merge(
            cf,
            on=["company_id", "year"],
            how="inner"
        )
    )

    print("=" * 60)
    print("DAY 12 DATA PREPARATION")
    print("=" * 60)
    print(f"P&L rows : {len(pnl)}")
    print(f"BS rows  : {len(bs)}")
    print(f"CF rows  : {len(cf)}")
    print(f"Merged   : {len(merged)}")

    return merged


def calculate_kpis(df):

    result = pd.DataFrame()

    result["company_id"] = df["company_id"]
    result["year"] = df["year"]

    # Profitability

    result["net_profit_margin_pct"] = df.apply(
        lambda r: net_profit_margin(
            r["net_profit"],
            r["sales"]
        ),
        axis=1
    )

    result["operating_profit_margin_pct"] = df.apply(
        lambda r: operating_profit_margin(
            r["operating_profit"],
            r["sales"]
        ),
        axis=1
    )

    result["return_on_equity_pct"] = df.apply(
        lambda r: return_on_equity(
            r["net_profit"],
            r["equity_capital"],
            r["reserves"]
        ),
        axis=1
    )

    # Leverage

    result["debt_to_equity"] = df.apply(
        lambda r: debt_to_equity(
            r["borrowings"],
            r["equity_capital"],
            r["reserves"]
        ),
        axis=1
    )

    result["interest_coverage"] = df.apply(
        lambda r: interest_coverage_ratio(
            r["operating_profit"],
            r["other_income"],
            r["interest"]
        ),
        axis=1
    )

    # Efficiency

    result["asset_turnover"] = df.apply(
        lambda r: asset_turnover(
            r["sales"],
            r["total_assets"]
        ),
        axis=1
    )

    # Cash Flow

    result["free_cash_flow_cr"] = df.apply(
        lambda r: free_cash_flow(
            r["operating_activity"],
            r["investing_activity"]
        ),
        axis=1
    )

    result["capex_cr"] = df["investing_activity"].abs()

    # Other KPIs

    result["earnings_per_share"] = df["eps"]

    result["book_value_per_share"] = (
        (df["equity_capital"] + df["reserves"])
        / df["equity_capital"].replace(0, pd.NA)
    )

    result["dividend_payout_ratio_pct"] = df["dividend_payout"]

    result["total_debt_cr"] = df["borrowings"]

    result["cash_from_operations_cr"] = df["operating_activity"]
    # -----------------------------
    # CAGR Calculations
    # -----------------------------

    result["revenue_cagr_5yr"] = None
    result["pat_cagr_5yr"] = None
    result["eps_cagr_5yr"] = None

    for company in df["company_id"].unique():

        company_df = df[df["company_id"] == company].sort_values("year")

        revenue_value, _ = revenue_cagr(company_df, 5)
        pat_value, _ = pat_cagr(company_df, 5)
        eps_value, _ = eps_cagr(company_df, 5)

        result.loc[
            result["company_id"] == company,
            "revenue_cagr_5yr"
        ] = revenue_value

        result.loc[
            result["company_id"] == company,
            "pat_cagr_5yr"
        ] = pat_value

        result.loc[
            result["company_id"] == company,
            "eps_cagr_5yr"
        ] = eps_value


    # -----------------------------
    # Composite Quality Score
    # -----------------------------

    result["composite_quality_score"] = result.apply(
        lambda r: composite_quality_score(
            r["return_on_equity_pct"],
            r["net_profit_margin_pct"],
            r["asset_turnover"],
            r["debt_to_equity"],
            r["interest_coverage"]
        ),
        axis=1
    )

    return result
def save_to_database(ratios):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    print("\nClearing existing financial_ratios table...")

    cursor.execute("DELETE FROM financial_ratios")

    conn.commit()

    print("Inserting new KPI data...")

    ratios.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM financial_ratios"
    )

    total = cursor.fetchone()[0]

    print("\n" + "=" * 60)
    print("DATABASE UPDATED")
    print("=" * 60)
    print(f"Rows inserted : {total}")

    sample = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        LIMIT 5
        """,
        conn
    )

    print("\nSample Data\n")
    print(sample)

    conn.close()


def main():

    merged = load_data()

    ratios = calculate_kpis(merged)
    print(ratios[["company_id", "year", "return_on_equity_pct"]].head(20))
    print(ratios["return_on_equity_pct"].describe())
    validator = FinancialValidator()
    detector = AnomalyDetector()
    report = ValidationReport()

    for _, row in ratios.iterrows():

        validation = validator.validate({
            "net_profit_margin": row["net_profit_margin_pct"],
            "operating_margin": row["operating_profit_margin_pct"],
            "roe": row["return_on_equity_pct"],
            "debt_to_equity": row["debt_to_equity"],
            "interest_coverage": row["interest_coverage"],
            "asset_turnover": row["asset_turnover"],
            "revenue_cagr": row["revenue_cagr_5yr"],
            "pat_cagr": row["pat_cagr_5yr"],
            "eps_cagr": row["eps_cagr_5yr"],
            "composite_quality_score": row["composite_quality_score"],
            # Required fields for validator
            "revenue": 1,
            "pat": 1,
            "total_assets": 1,
            "shareholders_equity": 1,
        })

        anomalies = detector.detect({
            "roe": row["return_on_equity_pct"],
            "debt_to_equity": row["debt_to_equity"],
            "asset_turnover": row["asset_turnover"],
            "interest_coverage": row["interest_coverage"],
        })

        report.add_company(
            row["company_id"],
            row["year"],
            validation,
            anomalies
        )

    report.export_csv()

    summary = report.summary()

    print("\nValidation Summary")
    print("-" * 40)
    print(f"Companies : {summary['companies']}")
    print(f"Errors    : {summary['errors']}")
    print(f"Warnings  : {summary['warnings']}")
    print(f"Anomalies : {summary['anomalies']}")

    print("\n" + "=" * 60)
    print("DAY 12 KPI CALCULATION")
    print("=" * 60)

    print(f"Calculated KPI Rows : {len(ratios)}")

    print("\nFirst Five Calculated Rows\n")

    print(ratios.head())

    save_to_database(ratios)

    print("\n" + "=" * 60)
    print("DAY 12 COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()