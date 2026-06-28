def asset_turnover(
    sales,
    assets
):
    if assets == 0:
        return None

    return round(
        sales / assets,
        2
    )


def equity_turnover(
    sales,
    equity
):
    if equity == 0:
        return None

    return round(
        sales / equity,
        2
    )
