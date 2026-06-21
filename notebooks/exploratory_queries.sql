-- Query 1
SELECT COUNT(*) AS total_companies
FROM companies;

-- Query 2
SELECT company_id,
       COUNT(*) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available;

-- Query 3
SELECT MIN(year) AS oldest_year,
       MAX(year) AS latest_year
FROM profitandloss;

-- Query 4
SELECT company_id,
       AVG(net_profit) AS avg_profit
FROM profitandloss
GROUP BY company_id
ORDER BY avg_profit DESC
LIMIT 10;

-- Query 5
SELECT company_id,
       AVG(sales) AS avg_sales
FROM profitandloss
GROUP BY company_id
ORDER BY avg_sales DESC
LIMIT 10;

-- Query 6
SELECT company_id,
       SUM(operating_cashflow) AS total_ocf
FROM cashflow
GROUP BY company_id
ORDER BY total_ocf DESC
LIMIT 10;

-- Query 7
SELECT broad_sector,
       COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- Query 8
SELECT COUNT(*) AS document_count
FROM documents;

-- Query 9
SELECT COUNT(*) AS stock_price_rows
FROM stock_prices;

-- Query 10
SELECT peer_group_name,
       COUNT(*) AS companies
FROM peer_groups
GROUP BY peer_group_name
ORDER BY companies DESC;