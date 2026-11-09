`top_n_per_region(df, n)` should return the `n` largest-`amount` rows **of each region** (columns unchanged), ordered by region ascending then amount descending, with a clean index. Right now it returns only `n` rows in total. Fix it.

SQL: `SELECT * FROM df QUALIFY ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) <= n ORDER BY region, amount DESC`.
