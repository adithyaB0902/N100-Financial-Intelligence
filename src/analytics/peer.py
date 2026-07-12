import sqlite3

import numpy as np
import pandas as pd


class PeerEngine:
    """
    Day 18
    Peer Percentile Ranking Engine

    Computes percentile rankings within each
    peer group and stores the results in
    peer_percentiles.
    """

    METRICS = [
    "return_on_equity_pct",
    "return_on_capital_employed",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover",
]

    def __init__(self, database_path):

        self.database_path = database_path

        self.conn = sqlite3.connect(database_path)

        self.financials = None
        self.peer_groups = None

        self.results = []

    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------

    def load_data(self):

        self.financials = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn
        )

        self.peer_groups = pd.read_sql(
            """
            SELECT
                company_id,
                peer_group_name
            FROM peer_groups
            """,
            self.conn
        )

        # Latest year only

        self.financials["year_num"] = (
            self.financials["year"]
            .astype(str)
            .str[-4:]
            .astype(int)
        )

        self.financials = (
            self.financials
            .sort_values("year_num")
            .drop_duplicates(
                subset="company_id",
                keep="last"
            )
            .drop(columns="year_num")
            .reset_index(drop=True)
        )

        # Merge peer groups

        self.financials = self.financials.merge(
            self.peer_groups,
            on="company_id",
            how="left"
        )

        # Companies without peer group

        self.financials["peer_group_name"] = (
            self.financials["peer_group_name"]
            .fillna("No peer group assigned")
        )

        return self.financials

    # --------------------------------------------------
    # Percent Rank
    # --------------------------------------------------

    @staticmethod
    def percent_rank(series):

        if len(series.dropna()) <= 1:

            return pd.Series(
                np.ones(len(series)) * 100,
                index=series.index
            )

        return (
            series.rank(method="average", pct=True)
            * 100
        )
        # --------------------------------------------------
    # Compute Peer Percentiles
    # --------------------------------------------------

    def compute_peer_percentiles(self):

        self.results = []

        for peer_group, group in self.financials.groupby("peer_group_name"):

            # Companies without peer group are skipped
            if peer_group == "No peer group assigned":
                print(
                    "No peer group assigned:",
                    len(group),
                    "company(s)"
                )
                continue

            print(
                f"Processing {peer_group} "
                f"({len(group)} companies)"
            )

            for metric in self.METRICS:

                if metric not in group.columns:
                    continue

                metric_df = group[
                    [
                        "company_id",
                        "year",
                        metric
                    ]
                ].copy()

                metric_df = metric_df.dropna(
                    subset=[metric]
                )

                if metric_df.empty:
                    continue

                # ------------------------------------------
                # Debt/Equity
                # Lower value is better
                # ------------------------------------------

                if metric == "debt_to_equity":

                    metric_df["percentile_rank"] = (
                        100
                        - self.percent_rank(
                            metric_df[metric]
                        )
                    )

                # ------------------------------------------
                # All other metrics
                # Higher is better
                # ------------------------------------------

                else:

                    metric_df["percentile_rank"] = (
                        self.percent_rank(
                            metric_df[metric]
                        )
                    )

                metric_df["peer_group_name"] = peer_group
                metric_df["metric"] = metric

                metric_df.rename(
                    columns={
                        metric: "value"
                    },
                    inplace=True
                )

                metric_df = metric_df[
                    [
                        "company_id",
                        "peer_group_name",
                        "metric",
                        "value",
                        "percentile_rank",
                        "year"
                    ]
                ]

                self.results.extend(
                    metric_df.to_dict("records")
                )

        self.results = pd.DataFrame(self.results)

        if not self.results.empty:

            self.results["percentile_rank"] = (
                self.results["percentile_rank"]
                .round(2)
            )

        return self.results
        # --------------------------------------------------
    # Save Results
    # --------------------------------------------------

    def save_to_database(self):

        if self.results is None or self.results.empty:
            print("No percentile results to save.")
            return

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM peer_percentiles
            """
        )

        self.results.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="append",
            index=False
        )

        self.conn.commit()

        print(
            f"\nSaved {len(self.results)} "
            f"peer percentile records."
        )

    # --------------------------------------------------
    # Run Complete Pipeline
    # --------------------------------------------------

    def run(self):

        print("=" * 60)
        print("DAY 18 - PEER PERCENTILE ENGINE")
        print("=" * 60)

        self.load_data()

        print(
            f"Loaded {len(self.financials)} latest company records."
        )

        self.compute_peer_percentiles()

        self.save_to_database()

        print("\nCompleted successfully.")

    # --------------------------------------------------
    # Close Database
    # --------------------------------------------------

    def close(self):

        if self.conn:
            self.conn.close()


# ------------------------------------------------------
# Main
# ------------------------------------------------------

if __name__ == "__main__":

    engine = PeerEngine("db/nifty100.db")

    try:
        engine.run()

    finally:
        engine.close()