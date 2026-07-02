import pandas as pd

from src.screener.filters import (
    high_roe,
    low_debt,
    positive_growth,
    high_quality,
    reasonable_roe,
    latest_year
)


class FinancialScreener:
    """
    Financial Screener

    Allows chaining multiple financial filters.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def high_roe(self, minimum=20):
        self.df = high_roe(self.df, minimum)
        return self

    def low_debt(self, maximum=1):
        self.df = low_debt(self.df, maximum)
        return self

    def positive_growth(self):
        self.df = positive_growth(self.df)
        return self

    def high_quality(self, minimum=70):
        self.df = high_quality(self.df, minimum)
        return self

    def reasonable_roe(self, minimum=-100, maximum=100):
        """
        Filter companies having a reasonable ROE range.
        """
        self.df = reasonable_roe(
            self.df,
            minimum,
            maximum
        )
        return self

    def reset(self, dataframe):
        """
        Reset screener with a fresh dataframe.
        """
        self.df = dataframe.copy()
        return self

    def get_results(self):
        """
        Return the filtered dataframe.
        """
        return self.df.copy()
    
    def latest_year(self):
        self.df = latest_year(self.df)
        return self

    def count(self):
        """
        Return number of companies after filtering.
        """
        return len(self.df)
    