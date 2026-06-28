import pandas as pd


def net_profit_margin(net_profit, sales):
    if sales == 0:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(op_profit, sales):
    if sales == 0:
        return None
    return round((op_profit / sales) * 100, 2)


def return_on_equity(net_profit, equity):
    if equity == 0:
        return None
    return round((net_profit / equity) * 100, 2)


def return_on_assets(net_profit, assets):
    if assets == 0:
        return None
    return round((net_profit / assets) * 100, 2)