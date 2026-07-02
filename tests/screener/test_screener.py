import pandas as pd

from src.screener.screener import FinancialScreener


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


def test_screener_chain():

    results = (
        FinancialScreener(sample_df())
        .latest_year()
        .reasonable_roe()
        .high_roe(20)
        .low_debt(1)
        .positive_growth()
        .high_quality(70)
        .get_results()
    )

    assert len(results) == 1
    assert results.iloc[0]["company_id"] == "A"


def test_count():

    screener = FinancialScreener(sample_df())

    assert screener.count() == 4


def test_reset():

    screener = FinancialScreener(sample_df())

    screener.high_roe(20)

    assert screener.count() < 4

    screener.reset(sample_df())

    assert screener.count() == 4