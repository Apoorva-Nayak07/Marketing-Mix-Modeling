-- MARKETING SPEND OPTIMIZATION: SQL QUERIES
-- Run: python3 -c "import sqlite3; ..." or load into any SQL tool
-- Business question: where is our marketing budget working hardest?

-- Q1: Total spend and total sales across the whole period (the headline numbers)
SELECT
  ROUND(SUM(TV), 0)      AS total_tv_spend,
  ROUND(SUM(Radio), 0)   AS total_radio_spend,
  ROUND(SUM(Banners), 0) AS total_banner_spend,
  ROUND(SUM(Sales), 0)   AS total_sales
FROM spend;

-- Q2: Average weekly spend per channel and share of total spend
SELECT
  ROUND(AVG(TV), 0)      AS avg_weekly_tv,
  ROUND(AVG(Radio), 0)   AS avg_weekly_radio,
  ROUND(AVG(Banners), 0) AS avg_weekly_banners,
  ROUND(100.0 * SUM(TV)      / (SUM(TV)+SUM(Radio)+SUM(Banners)), 1) AS tv_share_pct,
  ROUND(100.0 * SUM(Radio)   / (SUM(TV)+SUM(Radio)+SUM(Banners)), 1) AS radio_share_pct,
  ROUND(100.0 * SUM(Banners) / (SUM(TV)+SUM(Radio)+SUM(Banners)), 1) AS banner_share_pct
FROM spend;

-- Q3: Weeks with ZERO spend on a channel - what did sales look like without it?
-- (a simple way to eyeball each channel's baseline contribution)
SELECT
  'TV=0'      AS scenario, ROUND(AVG(Sales), 0) AS avg_sales, COUNT(*) AS n_weeks FROM spend WHERE TV = 0
UNION ALL
SELECT 'Radio=0',   ROUND(AVG(Sales), 0), COUNT(*) FROM spend WHERE Radio = 0
UNION ALL
SELECT 'Banners=0', ROUND(AVG(Sales), 0), COUNT(*) FROM spend WHERE Banners = 0
UNION ALL
SELECT 'All spend>0', ROUND(AVG(Sales), 0), COUNT(*) FROM spend WHERE TV > 0 AND Radio > 0 AND Banners > 0;

-- Q4: Top 10 sales weeks - what channels were active?
SELECT Date, TV, Radio, Banners, Sales
FROM spend
ORDER BY Sales DESC
LIMIT 10;

-- Q5: Rank weeks by sales-per-dollar-spent (rough efficiency signal per week)
SELECT
  Date, Sales, (TV + Radio + Banners) AS total_spend,
  ROUND(Sales / NULLIF((TV + Radio + Banners), 0), 2) AS sales_per_spend_dollar,
  RANK() OVER (ORDER BY Sales / NULLIF((TV + Radio + Banners), 0) DESC) AS efficiency_rank
FROM spend
WHERE (TV + Radio + Banners) > 0
ORDER BY efficiency_rank
LIMIT 10;

-- Q6: Quarter-level rollup (turning 200 weekly rows into a business-readable summary)
SELECT
  substr(Date, 1, 4) || '-Q' || ((CAST(substr(Date,6,2) AS INTEGER)-1)/3 + 1) AS year_quarter,
  ROUND(SUM(TV), 0) AS tv_spend, ROUND(SUM(Radio), 0) AS radio_spend,
  ROUND(SUM(Banners), 0) AS banner_spend, ROUND(SUM(Sales), 0) AS total_sales
FROM spend
GROUP BY year_quarter
ORDER BY year_quarter;
