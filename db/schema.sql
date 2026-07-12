PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS profitandloss (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    net_profit REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS balancesheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS cashflow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    operating_cashflow REAL,
    capex REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    remarks TEXT,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    document_type TEXT,
    url TEXT,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    category TEXT,
    description TEXT,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS sectors (
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    trade_date DATE,
    close_price REAL,
    volume INTEGER,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,

    -- Day 8 KPIs
    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,

    -- Day 9 KPIs
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,

    -- Day 10 KPIs
    revenue_cagr_5yr REAL,
    pat_cagr_5yr REAL,
    eps_cagr_5yr REAL,

    -- Day 11 KPIs
    free_cash_flow_cr REAL,
    capex_cr REAL,
    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,
    total_debt_cr REAL,
    cash_from_operations_cr REAL,
    revenue_cr REAL,
    net_profit_cr REAL,
    composite_quality_score REAL,
    cfo_quality_score TEXT,
    capex_intensity_pct REAL,
    capex_category TEXT,
    fcf_conversion_pct REAL,
    capital_allocation_pattern TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS peer_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    peer_group_name TEXT,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);
CREATE INDEX IF NOT EXISTS idx_pnl_company_year
ON profitandloss(company_id, year);

CREATE INDEX IF NOT EXISTS idx_bs_company_year
ON balancesheet(company_id, year);

CREATE INDEX IF NOT EXISTS idx_cf_company_year
ON cashflow(company_id, year);

CREATE INDEX IF NOT EXISTS idx_prices_company_date
ON stock_prices(company_id, trade_date);
CREATE TABLE IF NOT EXISTS peer_percentiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id TEXT NOT NULL,
    peer_group_name TEXT NOT NULL,

    metric TEXT NOT NULL,
    value REAL,
    percentile_rank REAL,

    year TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE INDEX IF NOT EXISTS idx_peer_percentiles_company
ON peer_percentiles(company_id);

CREATE INDEX IF NOT EXISTS idx_peer_percentiles_group
ON peer_percentiles(peer_group_name);

CREATE INDEX IF NOT EXISTS idx_peer_percentiles_metric
ON peer_percentiles(metric);
ALTER TABLE financial_ratios
ADD COLUMN return_on_capital_employed REAL;