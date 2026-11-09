SELECT name, sex, joinYear, ROW_NUMBER() OVER (PARTITION BY sex ORDER BY joinYear DESC) AS recency_rank FROM users ORDER BY sex, recency_rank;
