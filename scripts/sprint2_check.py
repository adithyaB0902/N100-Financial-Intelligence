import os
import sys
import sqlite3
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.analytics.generate_capital_allocation import main as generate_capital_allocation
from src.kpi.populate_financial_ratios import main as populate_financial_ratios
from src.screener.screener import FinancialScreener

DB_PATH = "db/nifty100.db"


def run_sprint2_checks():
    """Run the Sprint 2 verification checks and return the result."""
    failures = []

    if not os.path.exists("output/capital_allocation.csv") or not os.path.exists("output/ratio_edge_cases.log"):
        populate_financial_ratios()
        generate_capital_allocation()

    if not os.path.exists("output/capital_allocation.csv"):
        failures.append("capital_allocation.csv missing")

    if not os.path.exists("output/ratio_edge_cases.log"):
        failures.append("ratio_edge_cases.log missing")

    conn = sqlite3.connect(DB_PATH)
    try:
        row_count = conn.execute("SELECT COUNT(*) FROM financial_ratios").fetchone()[0]
        if row_count < 1100:
            failures.append(f"financial_ratios row count too low: {row_count}")

        cols = [r[1] for r in conn.execute("PRAGMA table_info(financial_ratios)").fetchall()]
        empty_columns = [
            col for col in [
                "cfo_quality_score",
                "capex_intensity_pct",
                "capex_category",
                "fcf_conversion_pct",
                "capital_allocation_pattern",
            ] if col in cols and conn.execute(f"SELECT COUNT(*) FROM financial_ratios WHERE {col} IS NULL").fetchone()[0] == row_count
        ]
        if empty_columns:
            failures.append(f"empty KPI columns: {', '.join(empty_columns)}")
    finally:
        conn.close()

    try:
        conn = sqlite3.connect(DB_PATH)
        ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()
        ratios = ratios.dropna(subset=["return_on_equity_pct", "debt_to_equity", "revenue_cagr_5yr", "pat_cagr_5yr", "composite_quality_score"])
        screener = FinancialScreener(ratios)
        screener.latest_year().high_roe(15).low_debt(1).positive_growth().high_quality(70)
        result_count = screener.count()
        if not 15 <= result_count <= 50:
            failures.append(f"screener returned {result_count} companies")
    except Exception as exc:
        failures.append(f"screener check failed: {exc}")

    result = {"passed": not failures, "failures": failures}
    if result["passed"]:
        print("SPRINT 2 PASSED")
    else:
        print("SPRINT 2 FAILED")
        for failure in failures:
            print(f"- {failure}")
    return result


if __name__ == "__main__":
    run_sprint2_checks()
