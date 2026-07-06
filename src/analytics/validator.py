"""
Financial KPI Validation Module

Performs:
- Missing value checks
- Range validation
- Business rule validation
"""


class FinancialValidator:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, field, message):
        self.errors.append({
            "field": field,
            "message": message
        })

    def warning(self, field, message):
        self.warnings.append({
            "field": field,
            "message": message
        })

    def validate(self, ratios: dict):
        self.errors.clear()
        self.warnings.clear()

        required = [
            "revenue",
            "pat",
            "total_assets",
            "shareholders_equity"
        ]

        for field in required:
            if ratios.get(field) is None:
                self.error(field, "Missing value")

        self._check_range(ratios, "net_profit_margin", -100, 100)
        self._check_range(ratios, "operating_margin", -100, 100)
        self._check_range(ratios, "roe", -200, 200)
        self._check_range(ratios, "revenue_cagr", -100, 500)
        self._check_range(ratios, "pat_cagr", -100, 500)
        self._check_range(ratios, "eps_cagr", -100, 500)
        self._check_range(ratios, "composite_quality_score", 0, 100)
        self._check_range(ratios, "debt_to_equity", 0, 5)
        self._check_range(ratios, "interest_coverage", 0, 100)

        return {
            "errors": self.errors,
            "warnings": self.warnings
        }

    def _check_range(self, ratios, field, minimum, maximum):
        value = ratios.get(field)

        if value is None:
            return

        if isinstance(value, str):
            return

        sector = ratios.get("sector") or ratios.get("broad_sector")
        if field == "debt_to_equity" and sector in {"Financials", "Financial", "Bank", "Banks"}:
            return

        if field == "interest_coverage" and value == 0:
            return

        if value < minimum or value > maximum:
            self.warning(
                field,
                f"{field} of {value} is outside the expected range ({minimum} to {maximum})"
            )