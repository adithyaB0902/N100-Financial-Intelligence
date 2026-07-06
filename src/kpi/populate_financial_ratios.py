import os
import sqlite3
import numpy as np
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
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    capex_category,
    fcf_conversion_rate,
    capital_allocation_pattern
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

    # --------------------------------------------------
    # DAY 11 - Cash Flow KPIs
    # --------------------------------------------------

    from src.analytics.cashflow_kpis import (
        cfo_quality_score,
        capex_intensity,
        fcf_conversion_rate,
        capital_allocation_pattern
    )

    result["cfo_quality_score"] = None
    result["capex_intensity_pct"] = None
    result["capex_category"] = None
    result["fcf_conversion_pct"] = None
    result["capital_allocation_pattern"] = None

    for company in result["company_id"].unique():

        company_rows = (
            result[result["company_id"] == company]
            .sort_values("year")
        )

        quality = cfo_quality_score(
            company_rows["cash_from_operations_cr"].tolist(),
            company_rows["net_profit"].tolist()
        )

        for index, row in company_rows.iterrows():

            result.loc[index, "cfo_quality_score"] = quality

            capex = capex_intensity(
                row["capex_cr"],
                row["revenue_cr"]
            )

            result.loc[index, "capex_intensity_pct"] = capex

            if capex is None:
                category = None
            elif capex < 3:
                category = "Asset Light"
            elif capex <= 8:
                category = "Moderate"
            else:
                category = "Capital Intensive"

            result.loc[index, "capex_category"] = category

            result.loc[index, "fcf_conversion_pct"] = (
                fcf_conversion_rate(
                    row["free_cash_flow_cr"],
                    row["operating_profit"]
                )
            )

            result.loc[index, "capital_allocation_pattern"] = (
                capital_allocation_pattern(
                    row["cash_from_operations_cr"],
                    row["capex_cr"],
                    row["financing_activity"],
                    quality
                )
            )
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
            r.get("operating_profit", r.get("operating_profit_margin_pct", 0)),
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
            r.get("operating_profit", 0),
            r.get("other_income", 0),
            r.get("interest", 0)
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

    # ---------------------------------
    # Additional Cash Flow KPIs
    # ---------------------------------
    # FIX: capex_intensity() was being called twice per row (once to check
    # for None, once to extract [0]). That's wasteful and risks inconsistent
    # results if the function ever has any randomness/state. Call it once
    # and reuse the value.

    def _capex_intensity(r):
        value = capex_intensity(r["investing_activity"], r["sales"])
        return value if value is not None else None

    result["capex_intensity_pct"] = df.apply(_capex_intensity, axis=1)
    result["capex_category"] = result["capex_intensity_pct"].apply(capex_category)

    result["fcf_conversion_pct"] = result.apply(
        lambda r: fcf_conversion_rate(
            r["free_cash_flow_cr"],
            r.get("operating_profit", r.get("operating_profit_margin_pct", 0))
        ),
        axis=1
    )

    # Other KPIs

    result["earnings_per_share"] = df["eps"]

    result["book_value_per_share"] = (
        (df["equity_capital"] + df["reserves"])
        / df["equity_capital"].replace(0, pd.NA)
    )

    result["dividend_payout_ratio_pct"] = df["dividend_payout"]

    result["total_debt_cr"] = df["borrowings"]

    result["cash_from_operations_cr"] = df["operating_activity"]

    # FIX: the validator later needs real revenue / PAT / total assets /
    # shareholders' equity, but main() was passing hardcoded 1s for these
    # because they weren't carried into the ratios frame. Carry the raw
    # figures through so validation actually checks real numbers.
    result["revenue_cr"] = df["sales"]
    result["net_profit_cr"] = df["net_profit"]
    result["total_assets_cr"] = df["total_assets"]
    result["shareholders_equity_cr"] = df["equity_capital"] + df["reserves"]

    # -----------------------------
    # CAGR Calculations
    # -----------------------------
    # FIX: initializing these as None keeps the column dtype as `object`
    # once floats get assigned into it row-by-row, which causes silent
    # issues downstream (describe(), to_sql dtype inference, plotting).
    # Assigning np.nan (a real float) directly makes pandas create a
    # proper float64 column right away. (pd.NA doesn't astype cleanly to
    # float64 on all pandas versions, so np.nan is used instead.)

    result["revenue_cagr_5yr"] = np.nan
    result["pat_cagr_5yr"] = np.nan
    result["eps_cagr_5yr"] = np.nan

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
    # NOTE: cfo_quality_score() returns a text label (e.g. "High Quality"),
    # not a number, so this column must stay as a generic/object dtype.
    # (This is different from the CAGR columns above, which are genuinely
    # numeric.) Using None keeps it as object dtype.
    result["cfo_quality_score"] = None

    for company in df["company_id"].unique():

        company_df = (
            df[df["company_id"] == company]
            .sort_values("year")
        )

        quality = cfo_quality_score(
            company_df.get("operating_activity", company_df.get("cash_from_operations_cr", pd.Series([None] * len(company_df)))).tolist(),
            company_df["net_profit"].tolist()
        )

        result.loc[
            result["company_id"] == company,
            "cfo_quality_score"
        ] = quality

    result["capital_allocation_pattern"] = result.apply(
        lambda r: capital_allocation_pattern(
            r.get("operating_activity", r.get("cash_from_operations_cr", 0)),
            r.get("investing_activity", r.get("capex_cr", 0)),
            r.get("financing_activity", 0),
            r["cfo_quality_score"],
        ),
        axis=1
    )

    return result


def write_ratio_edge_cases(ratios):
    """Write a lightweight edge-case log for key ratio deltas."""
    output_path = "output/ratio_edge_cases.log"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rows = []
    for _, row in ratios.iterrows():
        roe = row.get("return_on_equity_pct")
        if roe is not None and abs(roe) > 5:
            rows.append({
                "Company": row.get("company_id"),
                "Year": row.get("year"),
                "Ratio": "ROE",
                "Expected": "Within normal range",
                "Calculated": roe,
                "Difference": abs(roe),
                "Category": "Formula Difference",
            })

        roce = row.get("return_on_capital_employed_pct")
        if roce is not None and abs(roce) > 5:
            rows.append({
                "Company": row.get("company_id"),
                "Year": row.get("year"),
                "Ratio": "ROCE",
                "Expected": "Within normal range",
                "Calculated": roce,
                "Difference": abs(roce),
                "Category": "Formula Difference",
            })

    if rows:
        pd.DataFrame(rows).to_csv(output_path, sep="\t", index=False)
    else:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write("Company\tYear\tRatio\tExpected\tCalculated\tDifference\tCategory\n")


def save_to_database(ratios):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    print("\nClearing existing financial_ratios table...")

    cursor.execute("DELETE FROM financial_ratios")

    conn.commit()

    print("Inserting new KPI data...")

    cursor.execute("PRAGMA table_info(financial_ratios)")
    table_columns = [row[1] for row in cursor.fetchall()]

    save_frame = ratios.loc[:, ratios.columns.intersection(table_columns)]

    save_frame.to_sql(
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
            # FIX: these used to be hardcoded to 1, meaning validation was
            # silently checking dummy numbers instead of the real ones.
            # They're now taken from the columns computed in calculate_kpis.
            "revenue": row["revenue_cr"],
            "pat": row["net_profit_cr"],
            "total_assets": row["total_assets_cr"],
            "shareholders_equity": row["shareholders_equity_cr"],
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

    write_ratio_edge_cases(ratios)
    save_to_database(ratios)

    print("\n" + "=" * 60)
    print("DAY 12 COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()