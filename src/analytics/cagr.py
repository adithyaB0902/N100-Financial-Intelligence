"""
Sprint 2 - Day 10
CAGR Engine
"""


def calculate_cagr(start_value, end_value, years):
    """
    Generic CAGR Calculator

    Returns:
        (value, flag)
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start_value == 0:
        return None, "ZERO_BASE"

    if years < 3:
        return None, "INSUFFICIENT"

    # Positive → Positive
    if start_value > 0 and end_value > 0:

        cagr = (
            ((end_value / start_value) ** (1 / years))
            - 1
        ) * 100

        return round(cagr, 2), None

    # Positive → Negative
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative → Positive
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Negative → Negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"
def revenue_cagr(df, years):
    """
    Calculate Revenue CAGR from sales column.
    """
    if len(df) <= years:
        return None, "INSUFFICIENT"

    start = df.iloc[-(years + 1)]["sales"]
    end = df.iloc[-1]["sales"]

    return calculate_cagr(start, end, years)


def pat_cagr(df, years):
    """
    Calculate PAT CAGR from net_profit column.
    """
    if len(df) <= years:
        return None, "INSUFFICIENT"

    start = df.iloc[-(years + 1)]["net_profit"]
    end = df.iloc[-1]["net_profit"]

    return calculate_cagr(start, end, years)


def eps_cagr(df, years):
    """
    Calculate EPS CAGR from eps column.
    """
    if len(df) <= years:
        return None, "INSUFFICIENT"

    start = df.iloc[-(years + 1)]["eps"]
    end = df.iloc[-1]["eps"]

    return calculate_cagr(start, end, years)