import pandas as pd


def high_roe(df, minimum=20):
    """
    Return companies with ROE >= minimum.
    """
    return df[df["return_on_equity_pct"] >= minimum]
def low_debt(df, maximum=1):
    """
    Return companies with Debt-to-Equity <= maximum.
    """
    return df[df["debt_to_equity"] <= maximum]
def positive_growth(df):
    """
    Return companies with positive Revenue and PAT CAGR.
    """
    return df[
        (df["revenue_cagr_5yr"] > 0) &
        (df["pat_cagr_5yr"] > 0)
    ]
def high_quality(df, minimum=70):
    """
    Return companies with high composite quality score.
    """
    return df[df["composite_quality_score"] >= minimum]
def reasonable_roe(df, minimum=-100, maximum=100):
    """
    Filter companies having a reasonable ROE range.

    This avoids ranking companies with extremely high or
    low ROE caused by a very small equity base.
    """

    return df[
        (df["return_on_equity_pct"] >= minimum) &
        (df["return_on_equity_pct"] <= maximum)
    ]
def latest_year(df):
    temp = df.copy()
    temp["year_num"] = temp["year"].str.extract(r"(\d{4})").astype(int)

    result = (
        temp.sort_values("year_num")
            .groupby("company_id")
            .tail(1)
            .drop(columns=["year_num"])
            .reset_index(drop=True)
    )

    return result