def debt_to_equity(total_debt, equity):
    if equity == 0:
        return None

    return round(
        total_debt / equity,
        2
    )


def interest_coverage(
    ebit,
    interest_expense
):
    if interest_expense == 0:
        return None

    return round(
        ebit / interest_expense,
        2
    )
