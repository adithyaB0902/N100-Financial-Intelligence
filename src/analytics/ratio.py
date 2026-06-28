"""
Financial Ratio Engine
Sprint 2 - Day 8 & Day 9
"""


# =====================================================
# DAY 8 - PROFITABILITY RATIOS
# =====================================================

def net_profit_margin(net_profit, sales):
    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def validate_opm(calculated_opm, source_opm):
    if calculated_opm is None or source_opm is None:
        return True

    return abs(calculated_opm - source_opm) <= 1


def return_on_equity(net_profit, equity_capital, reserves):

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
):

    capital = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(
    net_profit,
    total_assets,
):

    if total_assets == 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2,
    )


# =====================================================
# DAY 9 - LEVERAGE & EFFICIENCY RATIOS
# =====================================================

def debt_to_equity(
    borrowings,
    equity_capital,
    reserves,
):

    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2,
    )


def high_leverage_flag(
    de_ratio,
    broad_sector,
):

    if de_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return de_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income)
        / interest,
        2,
    )


def icr_label(icr):

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning_flag(icr):

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings,
    investments,
):

    return round(
        borrowings - investments,
        2,
    )


def asset_turnover(
    sales,
    total_assets,
):

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2,
    )