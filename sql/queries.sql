
-- 1. Top 5 Funds by AUM
SELECT scheme_name, aum_crore
FROM scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV by Fund
SELECT amfi_code, AVG(nav) as avg_nav
FROM nav_history
GROUP BY amfi_code;

-- 3. Total SIP Inflow
SELECT SUM(sip_inflow_crore)
FROM monthly_sip_inflows;

-- 4. Transactions by State
SELECT state, COUNT(*) as total_transactions
FROM investor_transactions
GROUP BY state;

-- 5. Top 10 Cities
SELECT city, COUNT(*) as total
FROM investor_transactions
GROUP BY city
ORDER BY total DESC
LIMIT 10;

-- 6. Average Expense Ratio
SELECT AVG(expense_ratio_pct)
FROM scheme_performance;

-- 7. Highest Sharpe Ratio
SELECT scheme_name, sharpe_ratio
FROM scheme_performance
ORDER BY sharpe_ratio DESC
LIMIT 1;

-- 8. Funds by Risk Grade
SELECT risk_grade, COUNT(*)
FROM scheme_performance
GROUP BY risk_grade;

-- 9. Average Return by Category
SELECT category, AVG(return_3yr_pct)
FROM scheme_performance
GROUP BY category;

-- 10. Total Transactions Amount
SELECT SUM(amount_inr)
FROM investor_transactions;