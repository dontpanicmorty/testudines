SELECT name, price, ROUND(PERCENT_RANK() OVER (ORDER BY price), 2) AS price_pct_rank FROM items ORDER BY price DESC;
