from src.analytics.report_generator import ValidationReport
from src.analytics.validator import FinancialValidator

def test_summary():

    report = ValidationReport()

    report.add_company(
        "ABC",
        2025,
        {
            "errors": [],
            "warnings": [{"field": "roe", "message": "warning"}]
        },
        ["High ROE"]
    )

    summary = report.summary()

    assert summary["companies"] == 1
    assert summary["warnings"] == 1
    assert summary["anomalies"] == 1