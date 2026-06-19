
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

    # DQ-07
    def validate_net_cash(
        self,
        balance_df
    ):
        invalid_rows = balance_df[
            balance_df["cash"] < 0
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-07",
                "WARNING",
                "Negative cash balance",
                row["company_id"]
            )

    # DQ-08
    def validate_tax_rate(
        self,
        pnl_df
    ):
        invalid_rows = pnl_df[
            (pnl_df["tax_rate"] < 0) |
            (pnl_df["tax_rate"] > 100)
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-08",
                "WARNING",
                "Invalid tax rate",
                row["company_id"]
            )

    # DQ-09
    def validate_dividend(
        self,
        pnl_df
    ):
        invalid_rows = pnl_df[
            pnl_df["dividend"] >
            pnl_df["net_profit"]
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-09",
                "WARNING",
                "Dividend exceeds profit",
                row["company_id"]
            )

    # DQ-10
    def validate_urls(
        self,
        docs_df
    ):
        invalid_rows = docs_df[
            ~docs_df["url"].str.startswith(
                ("http://", "https://"),
                na=False
            )
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-10",
                "WARNING",
                "Invalid URL",
                row["company_id"]
            )

    # DQ-11
    def validate_eps_sign(
        self,
        pnl_df
    ):
        invalid_rows = pnl_df[
            (pnl_df["net_profit"] < 0) &
            (pnl_df["eps"] > 0)
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-11",
                "WARNING",
                "EPS sign mismatch",
                row["company_id"]
            )

    # DQ-12
    def validate_interest_coverage(
        self,
        pnl_df
    ):
        invalid_rows = pnl_df[
            pnl_df["interest_coverage"] < 0
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-12",
                "WARNING",
                "Negative interest coverage",
                row["company_id"]
            )

    # DQ-13
    def validate_year_range(
        self,
        df
    ):
        invalid_rows = df[
            (df["year"] < 2000) |
            (df["year"] > 2100)
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-13",
                "WARNING",
                "Year out of range",
                row["company_id"]
            )

    # DQ-14
    def validate_null_company_name(
        self,
        companies_df
    ):
        invalid_rows = companies_df[
            companies_df["company_name"].isnull()
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-14",
                "CRITICAL",
                "Missing company name",
                row["company_id"]
            )

    # DQ-15
    def validate_duplicate_ticker(
        self,
        companies_df
    ):
        duplicates = companies_df[
            companies_df["ticker"].duplicated()
        ]

        for _, row in duplicates.iterrows():
            self.add_failure(
                "DQ-15",
                "CRITICAL",
                "Duplicate ticker",
                row["ticker"]
            )

    # DQ-16
    def validate_profit_consistency(
        self,
        pnl_df
    ):
        invalid_rows = pnl_df[
            pnl_df["net_profit"] >
            pnl_df["sales"]
        ]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                "DQ-16",
                "WARNING",
                "Profit exceeds sales",
                row["company_id"]
            )
