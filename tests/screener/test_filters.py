import pandas as pd

from src.screener.filters import (
    high_roe,
    low_debt,
    positive_growth,
    high_quality,
    reasonable_roe,
    latest_year
)


def sample_df():
    return pd.DataFrame({
        "company_id": ["A", "A", "B", "B"],
        "year": ["Mar 2023", "Mar 2024", "Mar 2023", "Mar 2024"],
        "return_on_equity_pct": [25, 35, 10, 120],
        "debt_to_equity": [0.5, 0.8, 2.0, 0.3],
        "revenue_cagr_5yr": [10, 12, -5, 8],
        "pat_cagr_5yr": [8, 9, -2, 5],
        "composite_quality_score": [80, 90, 60, 95]
    })


def test_high_roe():
    df = high_roe(sample_df(), 20)
    assert len(df) == 3


def test_low_debt():
    df = low_debt(sample_df(), 1)
    assert len(df) == 3


def test_positive_growth():
    df = positive_growth(sample_df())
    assert len(df) == 3


def test_high_quality():
    df = high_quality(sample_df(), 70)
    assert len(df) == 3


def test_reasonable_roe():
    df = reasonable_roe(sample_df())
    assert len(df) == 3


def test_latest_year():
    df = latest_year(sample_df())
    assert len(df) == 2
    assert set(df["year"]) == {"Mar 2024"}