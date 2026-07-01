"""
Composite Quality Score

Score is out of 100.
Each KPI contributes equally.

Current Metrics:
1. ROE
2. Net Profit Margin
3. Asset Turnover
4. Debt-to-Equity
5. Interest Coverage
"""


def composite_quality_score(
    roe,
    npm,
    asset_turnover,
    debt_to_equity,
    interest_coverage
):
    score = 0

    # ROE
    if roe is not None:
        if roe >= 20:
            score += 20
        elif roe >= 15:
            score += 15
        elif roe >= 10:
            score += 10
        else:
            score += 5

    # Net Profit Margin
    if npm is not None:
        if npm >= 20:
            score += 20
        elif npm >= 10:
            score += 15
        elif npm >= 5:
            score += 10
        else:
            score += 5

    # Asset Turnover
    if asset_turnover is not None:
        if asset_turnover >= 2:
            score += 20
        elif asset_turnover >= 1:
            score += 15
        else:
            score += 10

    # Debt to Equity
    if debt_to_equity is not None:
        if debt_to_equity <= 0.5:
            score += 20
        elif debt_to_equity <= 1:
            score += 15
        elif debt_to_equity <= 2:
            score += 10
        else:
            score += 5

    # Interest Coverage
    if interest_coverage is not None:
        if interest_coverage >= 10:
            score += 20
        elif interest_coverage >= 5:
            score += 15
        elif interest_coverage >= 2:
            score += 10
        else:
            score += 5

    return score