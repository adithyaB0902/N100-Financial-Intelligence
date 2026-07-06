DROP TABLE IF EXISTS financial_ratios;

CREATE TABLE financial_ratios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id TEXT NOT NULL,
    year TEXT NOT NULL,

    --------------------------------------------------
    -- Profitability
    --------------------------------------------------

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,

    --------------------------------------------------
    -- Leverage
    --------------------------------------------------

    debt_to_equity REAL,
    interest_coverage REAL,

    --------------------------------------------------
    -- Efficiency
    --------------------------------------------------

    asset_turnover REAL,

    --------------------------------------------------
    -- Cash Flow
    --------------------------------------------------

    free_cash_flow_cr REAL,
    capex_cr REAL,

    --------------------------------------------------
    -- Shareholder Metrics
    --------------------------------------------------

    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,

    --------------------------------------------------
    -- Balance Sheet
    --------------------------------------------------

    total_debt_cr REAL,
    cash_from_operations_cr REAL,

    --------------------------------------------------
    -- Revenue & Profit
    --------------------------------------------------

    revenue_cr REAL,
    net_profit_cr REAL,

    --------------------------------------------------
    -- CAGR
    --------------------------------------------------

    revenue_cagr_5yr REAL,
    pat_cagr_5yr REAL,
    eps_cagr_5yr REAL,

    --------------------------------------------------
    -- Quality
    --------------------------------------------------

    composite_quality_score REAL,

    --------------------------------------------------
    -- Day 11 KPIs
    --------------------------------------------------

    cfo_quality_score TEXT,
    capex_intensity_pct REAL,
    capex_category TEXT,
    fcf_conversion_pct REAL,
    capital_allocation_pattern TEXT
);