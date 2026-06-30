def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    FCF = CFO + Investing Activity
    (Investing Activity is usually negative)
    """
    return operating_activity + investing_activity


def cfo_quality_score(
    cfo_values,
    pat_values
):
    """
    Average CFO/PAT over available years.
    """

    ratios = []

    for cfo, pat in zip(
        cfo_values,
        pat_values
    ):

        if pat == 0:
            continue

        ratios.append(
            cfo / pat
        )

    if len(ratios) == 0:
        return None

    avg = sum(ratios) / len(ratios)

    if avg > 1:
        return "High Quality"

    if avg >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity,
    sales
):

    if sales == 0:
        return None

    return abs(
        investing_activity
    ) / sales * 100


def capex_label(
    intensity
):

    if intensity is None:
        return None

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion(
    fcf,
    operating_profit
):

    if operating_profit == 0:
        return None

    return (
        fcf /
        operating_profit
    ) * 100


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_quality=None
):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    if signs == ("+", "-", "-"):

        if cfo_quality == "High Quality":
            return "Shareholder Returns"

        return "Reinvestor"

    if signs == ("+", "+", "-"):
        return "Liquidating Assets"

    if signs == ("-", "+", "+"):
        return "Distress Signal"

    if signs == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if signs == ("+", "+", "+"):
        return "Cash Accumulator"

    if signs == ("-", "-", "-"):
        return "Pre-Revenue"

    if signs == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"