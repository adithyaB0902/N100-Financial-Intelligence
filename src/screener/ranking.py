import pandas as pd


def rank_by_quality(df: pd.DataFrame):
    """
    Rank companies by overall quality.
    """

    return (
        df.sort_values(
            by=[
                "composite_quality_score",
                "return_on_equity_pct",
                "revenue_cagr_5yr",
                "pat_cagr_5yr"
            ],
            ascending=False
        )
        .reset_index(drop=True)
    )


def top_n(df: pd.DataFrame, n=10):
    """
    Return the top N ranked companies.
    """

    return rank_by_quality(df).head(n)