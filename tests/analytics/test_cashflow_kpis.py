import pytest

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    capex_label,
    fcf_conversion,
    capital_allocation_pattern
)


def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


def test_free_cash_flow_negative():
    assert free_cash_flow(100, -300) == -200


def test_cfo_quality_high():
    assert cfo_quality_score(
        [100, 120, 130],
        [80, 100, 110]
    ) == "High Quality"


def test_cfo_quality_moderate():
    assert cfo_quality_score(
        [50, 60],
        [100, 100]
    ) == "Moderate"


def test_cfo_quality_risk():
    assert cfo_quality_score(
        [20, 30],
        [100, 100]
    ) == "Accrual Risk"


def test_capex_intensity():
    assert capex_intensity(-50, 1000) == 5.0


def test_capex_label():
    assert capex_label(2.5) == "Asset Light"
    assert capex_label(5.0) == "Moderate"
    assert capex_label(12.0) == "Capital Intensive"


def test_fcf_conversion():
    assert fcf_conversion(100, 200) == 50.0


def test_fcf_conversion_zero():
    assert fcf_conversion(100, 0) is None


def test_pattern_reinvestor():
    assert capital_allocation_pattern(
        100,
        -50,
        -25
    ) == "Reinvestor"


def test_pattern_shareholder_returns():
    assert capital_allocation_pattern(
        100,
        -50,
        -25,
        "High Quality"
    ) == "Shareholder Returns"


def test_pattern_growth_debt():
    assert capital_allocation_pattern(
        -50,
        -100,
        200
    ) == "Growth Funded by Debt"