def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Free cash flow = CFO + investing activity.
    """
    return operating_activity + investing_activity


def cfo_quality_score(cfo_values, pat_values):
    """
    Average CFO/PAT over available years.
    """

    ratios = []

    for cfo, pat in zip(cfo_values, pat_values):
        if cfo is None or pat in (None, 0):
            continue

        ratios.append(cfo / pat)

    if not ratios:
        return None

    average = sum(ratios) / len(ratios)

    if average > 1:
        return "High Quality"

    if average >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    """Return capex intensity as a percentage of sales."""

    if sales in (None, 0):
        return None

    return round(abs(investing_activity) / sales * 100, 2)


def capex_label(intensity):
    """Return the capex intensity bucket label."""

    if intensity is None:
        return None

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"


def capex_category(intensity):
    """Compatibility wrapper for capex bucket classification."""
    return capex_label(intensity)


def fcf_conversion(fcf, operating_profit):
    """Return free cash flow conversion as a percentage."""

    if operating_profit in (None, 0):
        return None

    return round((fcf / operating_profit) * 100, 2)


def fcf_conversion_rate(free_cash_flow_value, operating_profit):
    """Compatibility wrapper for the percentage-based FCF conversion."""
    return fcf_conversion(free_cash_flow_value, operating_profit)


def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_quality=None
):
    """Classify the capital allocation pattern using the sign pattern."""

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Other"

  