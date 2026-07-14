import os
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RADAR_METRICS = [
    "return_on_equity_pct",
    "return_on_capital_employed",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score",
]

LABELS = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "PAT CAGR",
    "Revenue CAGR",
    "Composite",
]

OUTPUT_DIR = "reports/radar_charts"


class RadarEngine:

    def __init__(self, database_path="db/nifty100.db"):

        self.database_path = database_path
        self.conn = sqlite3.connect(database_path)

        self.financials = None
        self.peer_groups = None

        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def load_data(self):

        self.financials = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn,
        )

        self.peer_groups = pd.read_sql(
            """
            SELECT
                company_id,
                peer_group_name
            FROM peer_groups
            """,
            self.conn,
        )

        # Keep latest year only
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
                keep="last",
            )
            .drop(columns="year_num")
            .reset_index(drop=True)
        )

        self.financials = self.financials.merge(
            self.peer_groups,
            on="company_id",
            how="left",
        )

        return self.financials

    def normalize_metrics(self, df):

        normalized = df.copy()

        for metric in RADAR_METRICS:

            if metric not in normalized.columns:
                continue

            minimum = normalized[metric].min()
            maximum = normalized[metric].max()

            if (
                pd.isna(minimum)
                or pd.isna(maximum)
                or maximum == minimum
            ):
                normalized[metric] = 50
                continue

            normalized[metric] = (
                (normalized[metric] - minimum)
                / (maximum - minimum)
            ) * 100

        return normalized
    def plot_radar(self, company_row, reference_row, filename):

        values = company_row[RADAR_METRICS].fillna(0).tolist()
        reference = reference_row[RADAR_METRICS].fillna(0).tolist()

        # Close the radar polygon
        values += values[:1]
        reference += reference[:1]

        angles = np.linspace(
            0,
            2 * np.pi,
            len(RADAR_METRICS),
            endpoint=False
        ).tolist()

        angles += angles[:1]

        plt.figure(figsize=(8, 8))

        ax = plt.subplot(111, polar=True)

        # Company
        ax.plot(
            angles,
            values,
            linewidth=2,
            color="tab:blue",
            label=company_row["company_id"]
        )

        ax.fill(
            angles,
            values,
            alpha=0.25,
            color="tab:blue"
        )

        # Peer Average
        ax.plot(
            angles,
            reference,
            linestyle="--",
            linewidth=2,
            color="tab:red",
            label="Peer Average"
        )

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(LABELS, fontsize=10)

        ax.set_ylim(0, 100)

        plt.title(
            f"{company_row['company_id']} Radar Chart",
            fontsize=14
        )

        plt.legend(
            loc="upper right",
            bbox_to_anchor=(1.25, 1.10)
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(OUTPUT_DIR, filename),
            dpi=200
        )

        plt.close()
    def generate_all_charts(self):

        print("=" * 60)
        print("Generating Radar Charts")
        print("=" * 60)

        # Normalize metrics
        data = self.normalize_metrics(self.financials)

        # Overall Nifty 100 average
        overall_average = data[RADAR_METRICS].mean()

        generated = 0

        for _, company in data.iterrows():

            peer_group = company.get("peer_group_name")

            # Companies with a peer group
            if pd.notna(peer_group):

                peer_data = data[
                    data["peer_group_name"] == peer_group
                ]

                if len(peer_data) > 1:

                    reference = peer_data[
                        RADAR_METRICS
                    ].mean()

                else:
                    reference = overall_average

            # Companies without a peer group
            else:

                reference = overall_average

            self.plot_radar(
                company,
                reference,
                f"{company['company_id']}_radar.png"
            )

            generated += 1

        print(f"\nGenerated {generated} radar charts.")
    def run(self):

        print("=" * 60)
        print("DAY 19 - RADAR CHART ENGINE")
        print("=" * 60)

        self.load_data()

        print(
            f"Loaded {len(self.financials)} companies."
        )

        self.generate_all_charts()

        print("\nCompleted successfully.")
if __name__ == "__main__":

    engine = RadarEngine()

    try:
        engine.run()

    finally:
        engine.conn.close()