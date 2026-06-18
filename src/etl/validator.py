import pandas as pd


class DataValidator:

    def __init__(self):
        self.failures = []

    def add_failure(
        self,
        rule_id,
        severity,
        message,
        row_identifier=None
    ):
        self.failures.append({
            "rule_id": rule_id,
            "severity": severity,
            "message": message,
            "row_identifier": row_identifier
        })

    def export_failures(
        self,
        output_file="output/validation_failures.csv"
    ):
        df = pd.DataFrame(self.failures)
        df.to_csv(output_file, index=False)

    # DQ-01
    def validate_company_id_unique(
        self,
        companies_df
    ):
        duplicates = companies_df[
            companies_df["company_id"].duplicated()
        ]

        for _, row in duplicates.iterrows():
            self.add_failure(
                "DQ-01",
                "CRITICAL",
                "Duplicate company_id",
                row["company_id"]
            )

    # DQ-02
    def validate_company_year_unique(
        self,
        df
    ):
        duplicates = df[
            df.duplicated(
                subset=["company_id", "year"]
            )
        ]

        for _, row in duplicates.iterrows():
            self.add_failure(
                "DQ-02",
                "CRITICAL",
                "Duplicate company_id-year",
                f"{row['company_id']}_{row['year']}"
            )

    # DQ-03
    def validate_fk_integrity(
        self,
        child_df,
        companies_df
    ):
        valid_ids = set(
            companies_df["company_id"]
        )

        invalid_rows = child_df[
            ~child_df["company_id"].isin(valid_ids)
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-03",
                "CRITICAL",
                "Invalid company_id FK",
                row["company_id"]
            )

    # DQ-04
    def validate_balance_sheet(
        self,
        balance_df
    ):
        for _, row in balance_df.iterrows():

            assets = row["total_assets"]
            liabilities = row["total_liabilities"]
            equity = row["equity"]

            if assets == 0:
                continue

            diff = abs(
                assets - (liabilities + equity)
            )

            if diff / assets > 0.01:
                self.add_failure(
                    "DQ-04",
                    "WARNING",
                    "Balance sheet mismatch",
                    row["company_id"]
                )

    # DQ-05
    def validate_positive_sales(
        self,
        pnl_df
    ):
        invalid_rows = pnl_df[
            pnl_df["sales"] <= 0
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-05",
                "WARNING",
                "Sales <= 0",
                row["company_id"]
            )