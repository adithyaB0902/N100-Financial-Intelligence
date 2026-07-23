import re
from pathlib import Path

import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "analysis.xlsx"

OUTPUT_DIR = PROJECT_ROOT / "output"
VALIDATION_FILE = OUTPUT_DIR / "cagr_validation.csv"
OUTPUT_DIR.mkdir(exist_ok=True)

PARSED_FILE = OUTPUT_DIR / "analysis_parsed.csv"
FAILURE_FILE = OUTPUT_DIR / "parse_failures.csv"

# =====================================================
# Regex Pattern
# =====================================================

PATTERN = re.compile(
    r"(\d+)\s*Years?:?\s*([\d.]+)%",
    re.IGNORECASE,
)


# =====================================================
# Extract Percentage
# =====================================================

def extract_percentage(text):
    """
    Extract period (years) and percentage value from analysis text.

    Supported examples:
    -------------------
    10 Years: 21%
    5 Years 14%
    3 Years: 18.75%
    1 Year: -2%
    Last Year: 12%
    TTM: 43%

    Returns
    -------
    (period_years, value_pct)
    or None
    """

    if pd.isna(text):
        return None

    text = str(text).strip()

    # -------- 10 Years / 5 Years / 1 Year --------
    match = re.search(
        r"(\d+)\s*Years?:?\s*(-?[\d.]+)%",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            float(match.group(2)),
        )

    # -------- Last Year --------
    match = re.search(
        r"Last\s*Year:?\s*(-?[\d.]+)%",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            1,
            float(match.group(1)),
        )

    # -------- TTM --------
    match = re.search(
        r"TTM:?\s*(-?[\d.]+)%",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            0,
            float(match.group(1)),
        )

    return None
# =====================================================
# Load Analysis Excel
# =====================================================

def load_analysis_data():
    """
    Load analysis.xlsx and validate required columns.

    Returns
    -------
    pandas.DataFrame
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Analysis file not found:\n{DATA_PATH}"
        )

    df = pd.read_excel(
        DATA_PATH,
        header=1
    )

    # Standardize column names

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    required_columns = [
        "company_id",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df
# =====================================================
# Parse Analysis Sheet
# =====================================================

def parse_analysis_sheet(df):
    """
    Parse all CAGR text fields from analysis.xlsx.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    parsed_df
    failures_df
    """

    metric_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe",
    ]

    parsed_records = []
    failed_records = []

    for _, row in df.iterrows():

        company_id = row["company_id"]

        for metric in metric_columns:

            raw_text = row[metric]

            result = extract_percentage(raw_text)

            if result is None:

                failed_records.append(
                    {
                        "company_id": company_id,
                        "metric_type": metric,
                        "raw_text": raw_text,
                    }
                )

                continue

            period_years, value_pct = result

            parsed_records.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": period_years,
                    "value_pct": value_pct,
                }
            )

    parsed_df = pd.DataFrame(parsed_records)

    failures_df = pd.DataFrame(failed_records)

    return parsed_df, failures_df
# =====================================================
# Save Outputs
# =====================================================

def save_outputs(parsed_df, failures_df):

    parsed_df.to_csv(
        PARSED_FILE,
        index=False
    )

    failures_df.to_csv(
        FAILURE_FILE,
        index=False
    )

    print(f"\nSaved: {PARSED_FILE}")
    print(f"Saved: {FAILURE_FILE}")
# =====================================================
# Cross Validation Against Ratio Engine
# =====================================================

def validate_against_ratios(parsed_df):
    """
    Compare parsed CAGR values against Ratio Engine values.

    Flags differences greater than 5%.
    """

    print("\nRunning CAGR Validation...")

    # Import here to avoid circular imports
    import sqlite3

    db_path = PROJECT_ROOT / "db" / "nifty100.db"

    if not db_path.exists():
        print("Database not found. Skipping validation.")
        return

    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        company_id,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        return_on_equity_pct
    FROM financial_ratios
    """

    ratios = pd.read_sql(query, conn)

    conn.close()

    metric_mapping = {
        "compounded_sales_growth": "revenue_cagr_5yr",
        "compounded_profit_growth": "pat_cagr_5yr",
        "roe": "return_on_equity_pct",
    }

    validation_rows = []

    for _, row in parsed_df.iterrows():

        metric = row["metric_type"]

        if metric not in metric_mapping:
            continue

        ratio_column = metric_mapping[metric]

        company_rows = ratios[
            ratios["company_id"] == row["company_id"]
        ]

        if company_rows.empty:
            continue

        computed = company_rows.iloc[0][ratio_column]

        if pd.isna(computed):
            continue

        parsed = row["value_pct"]

        difference = abs(parsed - computed)

        validation_rows.append(
            {
                "company_id": row["company_id"],
                "metric_type": metric,
                "parsed_value": parsed,
                "computed_value": computed,
                "difference_pct": round(difference, 2),
                "status": (
                    "REVIEW"
                    if difference > 5
                    else "PASS"
                ),
            }
        )

    validation_df = pd.DataFrame(validation_rows)

    validation_df.to_csv(
        VALIDATION_FILE,
        index=False
    )

    print(f"Validation saved to {VALIDATION_FILE}")

    if not validation_df.empty:
        print(validation_df.head())

if __name__ == "__main__":

    print("=" * 60)
    print("NLP Analysis Parser")
    print("=" * 60)

    # Load Excel
    df = load_analysis_data()

    # Parse analysis text
    parsed_df, failures_df = parse_analysis_sheet(df)

    # Save parsed output and failures
    save_outputs(parsed_df, failures_df)

    print("\nSummary")
    print("-" * 60)
    print(f"Rows loaded      : {len(df)}")
    print(f"Rows parsed      : {len(parsed_df)}")
    print(f"Rows failed      : {len(failures_df)}")

    print("\nParsed Data Preview")
    print("-" * 60)
    print(parsed_df.head())

    if not failures_df.empty:
        print("\nFailures Preview")
        print("-" * 60)
        print(failures_df.head())
    else:
        print("\nNo parsing failures.")

    # Validate against Ratio Engine
    try:
        validate_against_ratios(parsed_df)
        print("\nCAGR validation completed successfully.")
    except Exception as e:
        print("\nCAGR validation skipped.")
        print(f"Reason: {e}")

    print("\n" + "=" * 60)
    print("Day 29 Parser Completed Successfully")
    print("=" * 60)