import sqlite3
import yaml
import pandas as pd

from src.screener.presets import PRESETS


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

        # Load sector information
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

        market_cap = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                market_cap_crore,
                pe_ratio,
                pb_ratio,
                dividend_yield_pct
            FROM market_cap
            """,
            conn
        )

        conn.close()

        # Merge sector information
        self.df = self.df.merge(
            self.sectors,
            on="company_id",
            how="left"
        )

        # Convert years to same format before merging
        # Convert market cap year
        market_cap["year"] = (
            market_cap["year"]
            .astype(str)
        )

        # Merge market cap only if year exists
        if "year" in self.df.columns:

            self.df["year"] = (
                self.df["year"]
                .astype(str)
                .str[-4:]
            )

            self.df = self.df.merge(
                market_cap,
                on=["company_id", "year"],
                how="left"
            )

        else:
            # Unit tests may not include year.
            # Merge using only company_id and keep the latest market-cap record.
            latest_market_cap = (
                market_cap.sort_values("year")
                .drop_duplicates(
                    subset="company_id",
                    keep="last"
                )
                .drop(columns="year")
            )

            self.df = self.df.merge(
                latest_market_cap,
                on="company_id",
                how="left"
            )

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config

    # --------------------------------------------------
    # Generic Filter Engine (Day 15)
    # --------------------------------------------------

    def apply_filters(self):

        filters = self.config["filters"]

        df = self.df.copy()

        minimum_filters = {
            "return_on_equity_pct": filters["roe_min"],
            "free_cash_flow_cr": filters["free_cash_flow_min"],
            "revenue_cagr_5yr": filters["revenue_cagr_5yr_min"],
            "pat_cagr_5yr": filters["pat_cagr_5yr_min"],
            "operating_profit_margin_pct": filters["operating_profit_margin_min"],
            "interest_coverage": filters["interest_coverage_min"],
            "asset_turnover": filters["asset_turnover_min"],
        }

        for column, minimum in minimum_filters.items():

            if column in df.columns:
                df = df[
                    df[column].fillna(-999999) >= minimum
                ]

        # Debt to Equity filter
        # Skip Financial companies

        if "debt_to_equity" in df.columns:

            financials = (
                df["broad_sector"]
                .fillna("")
                .str.lower()
                == "financials"
            )

            df = df[
                financials |
                (
                    df["debt_to_equity"].fillna(999999)
                    <= filters["debt_to_equity_max"]
                )
            ]

        # Interest Coverage
        # Debt Free companies automatically pass

        if "interest_coverage" in df.columns:

            df = df[
                (
                    df["interest_coverage"] >=
                    filters["interest_coverage_min"]
                )
                |
                (
                    df["interest_coverage"]
                    .astype(str)
                    .str.lower()
                    == "debt free"
                )
            ]

        # Latest year only

        if "year" in df.columns:

            def extract_year(value):
                try:
                    return int(str(value)[-4:])
                except Exception:
                    return 0

            df["year_num"] = df["year"].apply(extract_year)

            df = (
                df.sort_values("year_num")
                  .drop_duplicates(
                        subset="company_id",
                        keep="last"
                  )
                  .drop(columns="year_num")
            )

        # Sort

        sort_column = self.config["sort_by"]

        ascending = (
            self.config["sort_order"].lower()
            == "ascending"
        )

        if sort_column in df.columns:

            df = df.sort_values(
                by=sort_column,
                ascending=ascending
            )

        if "broad_sector" in df.columns:
            df = df.drop(columns=["broad_sector"])

        return df.reset_index(drop=True)

    # --------------------------------------------------
    # Day 16 Preset Screeners
    # --------------------------------------------------

    def apply_preset(self, preset_name):

        if preset_name not in PRESETS:
            raise ValueError(
                f"Unknown preset: {preset_name}"
            )

        preset = PRESETS[preset_name]

        df = self.df.copy()

        if (
            "roe_min" in preset
            and "return_on_equity_pct" in df.columns
        ):
            df = df[
                df["return_on_equity_pct"]
                >= preset["roe_min"]
            ]

        if (
            "debt_to_equity_max" in preset
            and "debt_to_equity" in df.columns
        ):

            financials = (
                df["broad_sector"]
                .fillna("")
                .str.lower()
                == "financials"
            )

            df = df[
                financials |
                (
                    df["debt_to_equity"]
                    <= preset["debt_to_equity_max"]
                )
            ]

        if (
            "free_cash_flow_min" in preset
            and "free_cash_flow_cr" in df.columns
        ):
            df = df[
                df["free_cash_flow_cr"]
                >= preset["free_cash_flow_min"]
            ]

        if (
            "revenue_cagr_5yr_min" in preset
            and "revenue_cagr_5yr" in df.columns
        ):
            df = df[
                df["revenue_cagr_5yr"]
                >= preset["revenue_cagr_5yr_min"]
            ]

        if (
            "pat_cagr_5yr_min" in preset
            and "pat_cagr_5yr" in df.columns
        ):
            df = df[
                df["pat_cagr_5yr"]
                >= preset["pat_cagr_5yr_min"]
            ]

        if (
            "pe_ratio_max" in preset
            and "pe_ratio" in df.columns
        ):
            df = df[
                df["pe_ratio"]
                <= preset["pe_ratio_max"]
            ]

        if (
            "pb_ratio_max" in preset
            and "pb_ratio" in df.columns
        ):
            df = df[
                df["pb_ratio"]
                <= preset["pb_ratio_max"]
            ]

        if (
            "dividend_yield_min" in preset
            and "dividend_yield_pct" in df.columns
        ):
            df = df[
                df["dividend_yield_pct"]
                >= preset["dividend_yield_min"]
            ]

        if (
            "dividend_payout_ratio_pct_max" in preset
            and "dividend_payout_ratio_pct" in df.columns
        ):
            df = df[
                df["dividend_payout_ratio_pct"]
                <= preset["dividend_payout_ratio_pct_max"]
            ]

        if (
            "revenue_min" in preset
            and "revenue_cr" in df.columns
        ):
            df = df[
                df["revenue_cr"]
                >= preset["revenue_min"]
            ]

        if "year" in df.columns:

            def extract_year(value):
                try:
                    return int(str(value)[-4:])
                except Exception:
                    return 0

            df["year_num"] = df["year"].apply(extract_year)

            df = (
                df.sort_values("year_num")
                  .drop_duplicates(
                        subset="company_id",
                        keep="last"
                  )
                  .drop(columns="year_num")
            )

        if "composite_quality_score" in df.columns:

            df = df.sort_values(
                "composite_quality_score",
                ascending=False
            )

        if "broad_sector" in df.columns:
            df = df.drop(columns=["broad_sector"])

        return df.reset_index(drop=True)