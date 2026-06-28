import pytest
import pandas as pd

from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)



def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)

    assert value is not None
    assert flag is None


def test_turnaround():
    value, flag = calculate_cagr(-100, 100, 5)

    assert value is None
    assert flag == "TURNAROUND"


def test_decline_to_loss():
    value, flag = calculate_cagr(100, -100, 5)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 5)

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 200, 5)

    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_years():
    value, flag = calculate_cagr(100, 200, 2)

    assert value is None
    assert flag == "INSUFFICIENT"


def test_invalid_years():
    value, flag = calculate_cagr(100, 200, 0)

    assert value is None
    assert flag == "INVALID_YEARS"


def test_same_values():
    value, flag = calculate_cagr(100, 100, 5)

    assert value == 0.0
    assert flag is None


def test_growth():
    value, flag = calculate_cagr(50, 150, 5)

    assert value > 0
    assert flag is None


def test_decline():
    value, flag = calculate_cagr(200, 100, 5)

    assert value < 0
    assert flag is None
def sample_dataframe():
    return pd.DataFrame(
        {
            "sales": [100, 120, 140, 160, 180, 200],
            "net_profit": [10, 12, 15, 18, 20, 25],
            "eps": [1, 1.2, 1.4, 1.6, 1.8, 2.0],
        }
    )


def test_revenue_cagr():
    value, flag = revenue_cagr(sample_dataframe(), 5)

    assert value is not None
    assert flag is None


def test_pat_cagr():
    value, flag = pat_cagr(sample_dataframe(), 5)

    assert value is not None
    assert flag is None


def test_eps_cagr():
    value, flag = eps_cagr(sample_dataframe(), 5)

    assert value is not None
    assert flag is None


def test_revenue_insufficient():
    df = pd.DataFrame({"sales": [100, 200]})

    value, flag = revenue_cagr(df, 5)

    assert value is None
    assert flag == "INSUFFICIENT"