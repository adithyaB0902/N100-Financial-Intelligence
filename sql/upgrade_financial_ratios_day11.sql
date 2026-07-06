-- Day 11 Cash Flow KPI Upgrade
ALTER TABLE financial_ratios
ADD COLUMN capex_intensity_pct REAL;

ALTER TABLE financial_ratios
ADD COLUMN fcf_conversion_pct REAL;

ALTER TABLE financial_ratios
ADD COLUMN cfo_quality_score TEXT;