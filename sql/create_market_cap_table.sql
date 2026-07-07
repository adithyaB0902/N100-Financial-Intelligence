DROP TABLE IF EXISTS market_cap;

CREATE TABLE market_cap (

    id INTEGER PRIMARY KEY,

    company_id TEXT,
    year TEXT,

    market_cap_crore REAL,
    enterprise_value_crore REAL,

    pe_ratio REAL,
    pb_ratio REAL,

    ev_ebitda REAL,

    dividend_yield_pct REAL
);