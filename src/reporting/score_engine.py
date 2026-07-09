import pandas as pd


class ScoreEngine:
    """
    Score Engine

    Features
    --------
    • P10/P90 Winsorization
    • 0-100 Normalization
    • Optional Sector Relative Normalization
    • Overall Weighted Score
    • Company Ranking
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    # --------------------------------------------------
    # Normalize KPI
    # --------------------------------------------------

    def normalize_score(
        self,
        column_name,
        sector_relative=False
    ):

        if column_name not in self.df.columns:
            raise ValueError(
                f"{column_name} not found."
            )

        score_column = column_name + "_score"

        # --------------------------------------------
        # Sector Relative Normalization
        # --------------------------------------------

        if (
            sector_relative
            and "broad_sector" in self.df.columns
        ):

            self.df[score_column] = (
                self.df
                .groupby("broad_sector")[column_name]
                .transform(self._winsorize_scale)
            )

        else:

            self.df[score_column] = self._winsorize_scale(
                self.df[column_name]
            )

    # --------------------------------------------------
    # Winsorization Helper
    # --------------------------------------------------

    def _winsorize_scale(self, values):

        values = values.astype(float)

        valid = values.dropna()

        if len(valid) == 0:
            return pd.Series(
                0,
                index=values.index,
                dtype=float
            )

        p10 = valid.quantile(0.10)
        p90 = valid.quantile(0.90)

        if p10 == p90:

            return pd.Series(
                100,
                index=values.index,
                dtype=float
            )

        clipped = values.clip(
            lower=p10,
            upper=p90
        )

        score = (
            (clipped - p10)
            /
            (p90 - p10)
        ) * 100

        score = (
            score
            .fillna(0)
            .clip(0, 100)
            .round(2)
        )

        return score

    # --------------------------------------------------
    # Overall Weighted Score
    # --------------------------------------------------

    def calculate_overall_score(self):

        required = [
            "return_on_equity_pct_score",
            "revenue_cagr_5yr_score",
            "composite_quality_score_score"
        ]

        for column in required:

            if column not in self.df.columns:
                raise ValueError(
                    f"{column} missing."
                )

            self.df[column] = (
                self.df[column]
                .fillna(0)
            )

        self.df["overall_score"] = (
            self.df["return_on_equity_pct_score"] * 0.40
            + self.df["revenue_cagr_5yr_score"] * 0.30
            + self.df["composite_quality_score_score"] * 0.30
        ).round(2)

    # --------------------------------------------------
    # Rank Companies
    # --------------------------------------------------

    def rank_companies(self):

        if "overall_score" not in self.df.columns:
            raise ValueError(
                "Run calculate_overall_score() first."
            )

        self.df["overall_score"] = (
            self.df["overall_score"]
            .fillna(0)
        )

        self.df["rank"] = (
            self.df["overall_score"]
            .rank(
                method="dense",
                ascending=False
            )
            .astype("Int64")
        )

        self.df = (
            self.df
            .sort_values(
                by=[
                    "rank",
                    "overall_score"
                ],
                ascending=[
                    True,
                    False
                ]
            )
            .reset_index(drop=True)
        )

    # --------------------------------------------------
    # Return DataFrame
    # --------------------------------------------------

    def get_dataframe(self):

        return self.df