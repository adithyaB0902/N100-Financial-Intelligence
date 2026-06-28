import pytest

from src.analytics.ratio import (
    net_profit_margin,
    operating_profit_margin,
    validate_opm,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
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
# =====================================================
# DAY 9 TESTS
# =====================================================

def test_debt_to_equity():
    assert debt_to_equity(200, 100, 100) == 1.0


def test_debt_free():
    assert debt_to_equity(0, 100, 100) == 0


def test_negative_equity_de():
    assert debt_to_equity(100, -100, 50) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6.0, "Industrials") is True


def test_financial_company_no_flag():
    assert high_leverage_flag(10.0, "Financials") is False


def test_interest_coverage():
    assert interest_coverage_ratio(
        100,
        20,
        10
    ) == 12.0


def test_interest_zero():
    assert interest_coverage_ratio(
        100,
        20,
        0
    ) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning_flag(1.2) is True


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0