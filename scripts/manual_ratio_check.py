import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def manual_ratio_check(company_id):
    """Print and return a manual ratio comparison for a company."""
    conn = sqlite3.connect(DB_PATH)
    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios WHERE company_id = ? ORDER BY year",
        conn,
        params=(company_id,),
    )
    conn.close()

    if ratios.empty:
        return {"company_id": company_id, "roe": None, "revenue_cagr": None, "pat_cagr": None, "eps_cagr": None}

    latest = ratios.iloc[-1]
    report = {
        "company_id": company_id,
        "roe": latest.get("return_on_equity_pct"),
        "revenue_cagr": latest.get("revenue_cagr_5yr"),
        "pat_cagr": latest.get("pat_cagr_5yr"),
        "eps_cagr": latest.get("eps_cagr_5yr"),
        "debt_to_equity": latest.get("debt_to_equity"),
        "interest_coverage": latest.get("interest_coverage"),
    }

    print(f"Manual ratio check for {company_id}")
    print(f"ROE: {report['roe']}")
    print(f"Revenue CAGR: {report['revenue_cagr']}")
    print(f"PAT CAGR: {report['pat_cagr']}")
    print(f"EPS CAGR: {report['eps_cagr']}")
    print(f"Debt to Equity: {report['debt_to_equity']}")
    print(f"Interest Coverage: {report['interest_coverage']}")
    return report


if __name__ == "__main__":
    import sys

    company_id = sys.argv[1] if len(sys.argv) > 1 else "TCS"
    manual_ratio_check(company_id)
