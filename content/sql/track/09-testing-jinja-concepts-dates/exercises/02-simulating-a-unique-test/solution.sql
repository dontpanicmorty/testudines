SELECT account_id, COUNT(*) AS n FROM accounts GROUP BY account_id HAVING COUNT(*) > 1 ORDER BY account_id;
