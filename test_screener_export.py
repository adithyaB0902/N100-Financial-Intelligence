import sqlite3
import pandas as pd

from src.reporting.score_engine import ScoreEngine
from src.reporting.screener_export import ScreenerExporter


def extract_year(value):
    try:
        return int(str(value)[-4:])
    except Exception:
        return 0


def main():

    print("=" * 60)
    print("DAY 17 - SCREENER EXPORT TEST")
    print("=" * 60)

    # ---------------------------------------
    # Load latest data
    # ---------------------------------------

    exporter = ScreenerExporter("db/nifty100.db")

    df = exporter.load_data()

    # ---------------------------------------
    # Score Engine
    # ---------------------------------------

    engine = ScoreEngine(df)

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

    engine.calculate_overall_score()

    engine.rank_companies()

    df = engine.get_dataframe()

    # ---------------------------------------
    # Presets
    # ---------------------------------------

    presets = {

        "Quality Compounder":
            df[df["overall_score"] >= 70],

        "Value Pick":
            df[df["overall_score"] >= 60],

        "Growth Accelerator":
            df[df["revenue_cagr_5yr"] >= 15],

        "Dividend Champion":
            df[df["dividend_payout_ratio_pct"] <= 60],

        "Debt Free Blue Chip":
            df[df["debt_to_equity"] <= 0.10],

        "Turnaround Watch":
            df[df["revenue_cagr_5yr"] >= 10]
    }

    exporter.export_excel(
        presets,
        "output/screener_output.xlsx"
    )

    print()

    for name, frame in presets.items():
        print(f"{name:<25} {len(frame)} companies")

    print("\nFinished.")


if __name__ == "__main__":
    main()