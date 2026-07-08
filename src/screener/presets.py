PRESETS = {

    # --------------------------------------------------
    # 1. Quality Compounder
    # --------------------------------------------------
    "quality_compounder": {
        "roe_min": 15,
        "debt_to_equity_max": 1.0,
        "free_cash_flow_min": 0,
        "revenue_cagr_5yr_min": 10
    },

    # --------------------------------------------------
    # 2. Value Pick
    # --------------------------------------------------
    "value_pick": {
        "pe_ratio_max": 20,
        "pb_ratio_max": 3,
        "debt_to_equity_max": 2.0,
        "dividend_yield_min": 1
    },

    # --------------------------------------------------
    # 3. Growth Accelerator
    # --------------------------------------------------
    "growth_accelerator": {
        "pat_cagr_5yr_min": 20,
        "revenue_cagr_5yr_min": 15,
        "debt_to_equity_max": 2.0
    },

    # --------------------------------------------------
    # 4. Dividend Champion
    # (Made stricter to reduce results)
    # --------------------------------------------------
    "dividend_champion": {
        "dividend_yield_min": 2.5,
        "dividend_payout_ratio_pct_max": 60,
        "free_cash_flow_min": 100,
        "roe_min": 15
    },

    # --------------------------------------------------
    # 5. Debt-Free Blue Chip
    # --------------------------------------------------
    "debt_free_blue_chip": {
        "debt_to_equity_max": 0,
        "roe_min": 12,
        "revenue_min": 5000
    },

    # --------------------------------------------------
    # 6. Turnaround Watch
    # (Made slightly stricter)
    # --------------------------------------------------
    "turnaround_watch": {
        "revenue_cagr_5yr_min": 15,
        "free_cash_flow_min": 100
    }

}