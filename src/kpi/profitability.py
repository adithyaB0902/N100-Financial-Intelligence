import pandas as pd


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)
    """
    if pd.isna(sales) or sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(op_profit, sales):
    """
    Operating Profit Margin (%)
    """
    if pd.isna(sales) or sales == 0:
        return None

    return round((op_profit / sales) * 100, 2)


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
    ROE = Net Profit / Shareholders' Equity × 100

    Shareholders' Equity = Equity Capital + Reserves
    """

    if pd.isna(equity_capital):
        equity_capital = 0

    if pd.isna(reserves):
        reserves = 0

    shareholders_equity = equity_capital + reserves

    if shareholders_equity == 0:
        return None

    return round((net_profit / shareholders_equity) * 100, 2)


def return_on_assets(net_profit, assets):
    """
    Return on Assets (ROA)
    """

    if pd.isna(assets) or assets == 0:
        return None

    return round((net_profit / assets) * 100, 2)


def return_on_capital_employed(
    operating_profit,
    borrowings,
    equity_capital,
    reserves
):
    """
    Return on Capital Employed (ROCE)

    Formula:
    ROCE = Operating Profit / Capital Employed × 100

    Capital Employed = Borrowings + Equity Capital + Reserves
    """

    if pd.isna(borrowings):
        borrowings = 0

    if pd.isna(equity_capital):
        equity_capital = 0

    if pd.isna(reserves):
        reserves = 0

    capital_employed = (
        borrowings +
        equity_capital +
        reserves
    )

    if capital_employed == 0:
        return None

    return round(
        (operating_profit / capital_employed) * 100,
        2
    )