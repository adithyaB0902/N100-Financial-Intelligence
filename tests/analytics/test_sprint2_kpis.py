import os

from src.analytics.cashflow_kpis import (
    capital_allocation_pattern,
    capex_category,
    fcf_conversion_rate,
)
from scripts.manual_ratio_check import manual_ratio_check
from scripts.sprint2_check import run_sprint2_checks


def test_capital_allocation_pattern():
    assert capital_allocation_pattern(100, -50, -25) == "Reinvestor"
    assert capital_allocation_pattern(100, -50, -25, "High Quality") == "Shareholder Returns"


def test_capex_category():
    assert capex_category(2.5) == "Asset Light"
    assert capex_category(5.0) == "Moderate"
    assert capex_category(12.0) == "Capital Intensive"


def test_fcf_conversion_rate():
    assert fcf_conversion_rate(100, 200) == 50.0


def test_manual_ratio_check():
    report = manual_ratio_check("TCS")
    assert report["company_id"] == "TCS"
    assert "roe" in report
    assert "revenue_cagr" in report
    assert "pat_cagr" in report
    assert "eps_cagr" in report


def test_sprint2_check():
    result = run_sprint2_checks()
    assert result["passed"] is True
    assert os.path.exists("output/ratio_edge_cases.log")
