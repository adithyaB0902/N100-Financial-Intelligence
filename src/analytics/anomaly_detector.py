"""
Financial Anomaly Detector

Detects unusual KPI values that may indicate
bad data or require manual review.
"""


class AnomalyDetector:

    def detect(self, ratios: dict):
        anomalies = []

        # ROE
        roe = ratios.get("roe")
        if roe is not None and abs(roe) > 100:
            anomalies.append(
                f"ROE unusually high ({roe})"
            )

        # Debt to Equity
        dte = ratios.get("debt_to_equity")
        if dte is not None and dte > 10:
            anomalies.append(
                f"Debt-to-Equity unusually high ({dte})"
            )

        # Asset Turnover
        at = ratios.get("asset_turnover")
        if at is not None and at < 0:
            anomalies.append(
                f"Negative Asset Turnover ({at})"
            )

        # Interest Coverage
        ic = ratios.get("interest_coverage")
        if ic is not None and ic > 100:
            anomalies.append(
                f"Interest Coverage unusually high ({ic})"
            )

        return anomalies