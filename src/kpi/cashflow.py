def free_cash_flow(
    operating_cashflow,
    capex
):
    return round(
        operating_cashflow - capex,
        2
    )


def cash_conversion_ratio(
    operating_cashflow,
    net_profit
):
    if net_profit == 0:
        return None

    return round(
        operating_cashflow / net_profit,
        2
    )
