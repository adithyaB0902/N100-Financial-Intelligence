import pytest

from src.analytics.ratio import (
    net_profit_margin,
    operating_profit_margin,
    validate_opm,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)


# -----------------------------
# Net Profit Margin
# -----------------------------

def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# -----------------------------
# Operating Profit Margin
# -----------------------------

def test_operating_profit_margin_normal():
    assert operating_profit_margin(200, 1000) == 20.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(200, 0) is None


# -----------------------------
# OPM Validation
# -----------------------------

def test_validate_opm_match():
    assert validate_opm(20.0, 20.5) is True


def test_validate_opm_mismatch():
    assert validate_opm(20.0, 22.5) is False


# -----------------------------
# Return on Equity (ROE)
# -----------------------------

def test_return_on_equity_normal():
    # Equity = 200 + 300 = 500
    # ROE = (100 / 500) * 100 = 20%
    assert return_on_equity(100, 200, 300) == 20.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -100, 50) is None


# -----------------------------
# Return on Capital Employed (ROCE)
# -----------------------------

def test_return_on_capital_employed_normal():
    # Capital = 200 + 300 + 500 = 1000
    # ROCE = (150 / 1000) * 100 = 15%
    assert return_on_capital_employed(
        150,
        200,
        300,
        500,
    ) == 15.0


def test_return_on_capital_employed_zero_capital():
    assert return_on_capital_employed(
        100,
        0,
        0,
        0,
    ) is None


# -----------------------------
# Return on Assets (ROA)
# -----------------------------

def test_return_on_assets_normal():
    assert return_on_assets(100, 1000) == 10.0


def test_return_on_assets_zero_assets():
    assert return_on_assets(100, 0) is None