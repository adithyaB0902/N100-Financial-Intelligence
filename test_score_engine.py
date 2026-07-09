import sqlite3
import pandas as pd

from src.reporting.score_engine import ScoreEngine


def main():

    conn = sqlite3.connect("db/nifty100.db")

    # --------------------------------------------------
    # Load Financial Ratios + Sector Information
    # --------------------------------------------------

    df = pd.read_sql(
        """
        SELECT
            fr.company_id,
            fr.year,
            s.broad_sector,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.revenue_cagr_5yr,
            fr.composite_quality_score
        FROM financial_ratios fr
        LEFT JOIN sectors s
            ON fr.company_id = s.company_id
        """,
        conn
    )

    conn.close()

    # --------------------------------------------------
    # Keep only latest financial year per company
    # --------------------------------------------------

    def extract_year(value):
        try:
            return int(str(value)[-4:])
        except Exception:
            return 0

    df["year_num"] = df["year"].apply(extract_year)

    df = (
        df.sort_values("year_num")
        .drop_duplicates(
            subset="company_id",
            keep="last"
        )
        .drop(columns=["year_num"])
        .reset_index(drop=True)
    )

    print("=" * 60)
    print("DAY 17 - SCORE ENGINE TEST")
    print("=" * 60)

    print("\nCompanies Ranked:", len(df))

    # --------------------------------------------------
    # Initialize Score Engine
    # --------------------------------------------------

    engine = ScoreEngine(df)

    # --------------------------------------------------
    # Sector Relative Normalization
    # --------------------------------------------------

    engine.normalize_score(
        "return_on_equity_pct",
        sector_relative=True
    )

    engine.normalize_score(
        "revenue_cagr_5yr",
        sector_relative=True
    )

    engine.normalize_score(
        "composite_quality_score",
        sector_relative=True
    )

    # --------------------------------------------------
    # Overall Score
    # --------------------------------------------------

    engine.calculate_overall_score()

    # --------------------------------------------------
    # Ranking
    # --------------------------------------------------

    engine.rank_companies()

    result = engine.get_dataframe()

    print("\nTop 10 Ranked Companies\n")

    print(
        result[
            [
                "rank",
                "company_id",
                "broad_sector",
                "year",
                "return_on_equity_pct",
                "return_on_equity_pct_score",
                "revenue_cagr_5yr",
                "revenue_cagr_5yr_score",
                "composite_quality_score",
                "composite_quality_score_score",
                "overall_score",
            ]
        ].head(10)
    )

    print("\nScore Summary\n")

    print(
        result[
            [
                "return_on_equity_pct_score",
                "revenue_cagr_5yr_score",
                "composite_quality_score_score",
                "overall_score",
            ]
        ].describe()
    )

    print("\nTop 10 Overall Ranked Companies\n")

    print(
        result[
            [
                "rank",
                "company_id",
                "broad_sector",
                "year",
                "overall_score",
            ]
        ].head(10)
    )

    print("\nSector Distribution\n")

    print(
        result["broad_sector"]
        .value_counts()
        .sort_index()
    )


if __name__ == "__main__":
    main()