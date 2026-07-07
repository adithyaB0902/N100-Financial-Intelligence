import sqlite3

import yaml
import pandas as pd


class ScreenerEngine:
    """
    Generic Financial Screener Engine
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        config_path="config/screener_config.yaml"
    ):

        self.df = dataframe.copy()

        conn = sqlite3.connect("db/nifty100.db")
        self.sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            conn
        )
        conn.close()
        self.df = self.df.merge(
            self.sectors,
            on="company_id",
            how="left"
        )

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config

    def apply_filters(self):

        filters = self.config["filters"]

        df = self.df.copy()

        # -----------------------------
        # Minimum Threshold Filters
        # -----------------------------

        minimum_filters = {
            "return_on_equity_pct": filters["roe_min"],
            "free_cash_flow_cr": filters["free_cash_flow_min"],
            "revenue_cagr_5yr": filters["revenue_cagr_5yr_min"],
            "pat_cagr_5yr": filters["pat_cagr_5yr_min"],
            "operating_profit_margin_pct": filters["operating_profit_margin_min"],
            "interest_coverage": filters["interest_coverage_min"],
            "asset_turnover": filters["asset_turnover_min"]
        }

        for column, minimum in minimum_filters.items():

            if column in df.columns:
                df = df[df[column].fillna(-999999) >= minimum]

        # -----------------------------
        # Maximum Threshold Filters
        # -----------------------------

        maximum_filters = {
            "debt_to_equity": filters["debt_to_equity_max"]
        }

        for column, maximum in maximum_filters.items():

            if column in df.columns:
                financials = (
                    df["broad_sector"]
                    .fillna("")
                    .str.lower()
                    == "financials"
                )
                df = df[
                    financials |
                    (
                        df[column].fillna(999999) <= maximum
                    )
                ]

        # -----------------------------
        # Sort Results
        # -----------------------------

        sort_column = self.config["sort_by"]

        ascending = (
            self.config["sort_order"].lower() == "ascending"
        )

        if sort_column in df.columns:

            df = df.sort_values(
                by=sort_column,
                ascending=ascending
            )
        # ---------------------------------
        # Keep only latest year per company
        # ---------------------------------

        if "year" in df.columns:

            def extract_year(x):
                try:
                    return int(str(x)[-4:])
                except:
                    return 0

            df["year_num"] = df["year"].apply(extract_year)

            df = (
                df.sort_values("year_num")
                  .drop_duplicates("company_id", keep="last")
                  .drop(columns=["year_num"])
            )

        if "broad_sector" in df.columns:
            df = df.drop(columns=["broad_sector"])

        return df.reset_index(drop=True)