import pandas as pd

from src.screener.ranking import (
    rank_by_quality,
    top_n
)


def sample_df():
    return pd.DataFrame({
        "company_id": ["A", "B", "C"],
        "composite_quality_score": [80, 95, 90],
        "return_on_equity_pct": [20, 30, 25],
        "revenue_cagr_5yr": [10, 15, 12],
        "pat_cagr_5yr": [8, 14, 11]
    })


def test_rank_by_quality():

    ranked = rank_by_quality(sample_df())

    assert ranked.iloc[0]["company_id"] == "B"
    assert ranked.iloc[1]["company_id"] == "C"
    assert ranked.iloc[2]["company_id"] == "A"


def test_top_n():

    ranked = top_n(sample_df(), 2)

    assert len(ranked) == 2
    assert list(ranked["company_id"]) == ["B", "C"]