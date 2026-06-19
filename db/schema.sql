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
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    roce REAL,
    de_ratio REAL,
    current_ratio REAL,
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
