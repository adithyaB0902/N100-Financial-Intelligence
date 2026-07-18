from pathlib import Path
import sqlite3

import pandas as pd


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================================
# DATABASE
# ==========================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ==========================================================
# LOAD TABLES
# ==========================================================

def load_market_cap():

    with get_connection() as conn:

        return pd.read_sql(
            """
            SELECT *
            FROM market_cap
            """,
            conn,
        )


def load_financial_ratios():

    with get_connection() as conn:

        return pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            conn,
        )


def load_companies():

    with get_connection() as conn:

        return pd.read_sql(
            """
            SELECT
                id,
                company_name
            FROM companies
            """,
            conn,
        )


def load_sectors():

    with get_connection() as conn:

        return pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            conn,
        )


# ==========================================================
# KEEP LATEST YEAR
# ==========================================================

def latest_market_cap(df):

    df = df.copy()

    df["year_num"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(int)
    )

    df = (
        df.sort_values("year_num")
        .drop_duplicates(
            subset="company_id",
            keep="last",
        )
    )

    return df


def latest_financial_ratios(df):

    df = df.copy()

    df["year_num"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(int)
    )

    df = (
        df.sort_values("year_num")
        .drop_duplicates(
            subset="company_id",
            keep="last",
        )
    )

    return df


# ==========================================================
# BUILD MASTER DATASET
# ==========================================================

def build_master_dataframe():

    market = latest_market_cap(
        load_market_cap()
    )

    ratios = latest_financial_ratios(
        load_financial_ratios()
    )

    companies = load_companies()

    sectors = load_sectors()

    df = market.merge(

        ratios,

        on="company_id",

        suffixes=(
            "_market",
            "_ratio",
        ),

        how="inner",

    )

    df = df.merge(

        companies,

        left_on="company_id",

        right_on="id",

        how="left",

    )

    if "id" in df.columns:

        df.drop(
            columns="id",
            inplace=True,
        )

    df = df.merge(

        sectors,

        on="company_id",

        how="left",

    )

    return df
# ==========================================================
# FCF YIELD
# ==========================================================

def compute_fcf_yield(df):

    df = df.copy()

    df["FCF_yield_pct"] = (
        df["free_cash_flow_cr"]
        / df["market_cap_crore"]
    ) * 100

    return df


# ==========================================================
# SECTOR MEDIAN P/E
# ==========================================================

def compute_sector_median_pe(df):

    sector_pe = (

        df.groupby("broad_sector")["pe_ratio"]

        .median()

        .reset_index()

        .rename(
            columns={
                "pe_ratio": "sector_median_pe"
            }
        )

    )

    df = df.merge(

        sector_pe,

        on="broad_sector",

        how="left"

    )

    return df


# ==========================================================
# P/E vs SECTOR MEDIAN
# ==========================================================

def compute_pe_difference(df):

    df = df.copy()

    df["PE_vs_sector_median_pct"] = (

        (
            df["pe_ratio"]
            - df["sector_median_pe"]
        )

        / df["sector_median_pe"]

    ) * 100

    return df


# ==========================================================
# VALUATION FLAGS
# ==========================================================

def assign_flags(df):

    flags = []

    for _, row in df.iterrows():

        pe = row["pe_ratio"]

        median = row["sector_median_pe"]

        if pd.isna(pe) or pd.isna(median):

            flags.append("Fair")

            continue

        if pe > median * 1.5:

            flags.append("Caution")

        elif pe < median * 0.7:

            flags.append("Discount")

        else:

            flags.append("Fair")

    df["flag"] = flags

    return df


# ==========================================================
# COMPLETE VALUATION PIPELINE
# ==========================================================

def calculate_valuation():

    df = build_master_dataframe()

    df = compute_fcf_yield(df)

    df = compute_sector_median_pe(df)

    df = compute_pe_difference(df)

    df = assign_flags(df)

    return df
# ==========================================================
# EXPORT FILES
# ==========================================================

def export_outputs(df):

    summary = df.copy()

    summary = summary[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "FCF_yield_pct",
            "sector_median_pe",
            "PE_vs_sector_median_pct",
            "flag",
        ]
    ].rename(
        columns={
            "broad_sector": "sector",
            "pe_ratio": "P/E",
            "pb_ratio": "P/B",
            "ev_ebitda": "EV/EBITDA",
            "sector_median_pe": "5yr_median_PE",
        }
    )

    summary = summary.sort_values(
        ["sector", "company_name"]
    )

    summary_path = OUTPUT_DIR / "valuation_summary.xlsx"

    summary.to_excel(
        summary_path,
        index=False,
    )

    flags = summary[
        summary["flag"].isin(
            [
                "Caution",
                "Discount",
            ]
        )
    ].copy()

    flags_path = OUTPUT_DIR / "valuation_flags.csv"

    flags.to_csv(
        flags_path,
        index=False,
    )

    return summary_path, flags_path


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("VALUATION MODULE")
    print("=" * 60)

    df = calculate_valuation()

    summary_file, flags_file = export_outputs(df)

    print(f"Companies processed : {len(df)}")
    print(f"Caution flags      : {(df['flag'] == 'Caution').sum()}")
    print(f"Discount flags     : {(df['flag'] == 'Discount').sum()}")
    print(f"Fair valuation     : {(df['flag'] == 'Fair').sum()}")

    print()
    print("Generated files:")
    print(summary_file)
    print(flags_file)

    print()
    print("Valuation module completed successfully.")


if __name__ == "__main__":
    main()