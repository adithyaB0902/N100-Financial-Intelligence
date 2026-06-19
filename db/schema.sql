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