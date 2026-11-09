SELECT name, rating, RANK() OVER (ORDER BY rating DESC) AS rating_rank FROM sellers ORDER BY rating_rank;
