SELECT
    category,
    SUM(revenue) AS revenue,
    SUM(profit) AS profit,
    SUM(profit) / NULLIF(SUM(revenue), 0) AS profit_margin
FROM sales
GROUP BY category
ORDER BY revenue DESC;