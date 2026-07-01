import os
import pandas as pd


class ValidationReport:

    def __init__(self):
        self.records = []

    def add_company(
        self,
        company,
        year,
        validation_result,
        anomalies
    ):
        self.records.append({
            "company": company,
            "year": year,
            "errors": validation_result["errors"],
            "warnings": validation_result["warnings"],
            "anomalies": anomalies
        })

    def summary(self):

        companies = len(self.records)

        errors = sum(
            len(r["errors"])
            for r in self.records
        )

        warnings = sum(
            len(r["warnings"])
            for r in self.records
        )

        anomalies = sum(
            len(r["anomalies"])
            for r in self.records
        )

        return {
            "companies": companies,
            "errors": errors,
            "warnings": warnings,
            "anomalies": anomalies
        }
    def export_csv(self, output_path="output/validation_report.csv"):
        rows = []

        for record in self.records:
            company = record["company"]
            year = record["year"]

            # Errors
            for error in record["errors"]:
                rows.append({
                    "Company": company,
                    "Year": year,
                    "Type": "Error",
                    "Field": error["field"],
                    "Message": error["message"]
                })

            # Warnings
            for warning in record["warnings"]:
                rows.append({
                    "Company": company,
                    "Year": year,
                    "Type": "Warning",
                    "Field": warning["field"],
                    "Message": warning["message"]
                })

            # Anomalies
            for anomaly in record["anomalies"]:
                rows.append({
                    "Company": company,
                    "Year": year,
                    "Type": "Anomaly",
                    "Field": "",
                    "Message": anomaly
                })

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)

        return output_path