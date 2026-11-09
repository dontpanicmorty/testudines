# SQL, pandas, polars and DuckDB side by side

DuckDB speaks SQL, so the SQL column is also the DuckDB column. Assume `df` is a table/frame called `orders` with columns `order_id, customer_id, status, amount`.

## Core operations

| Operation | SQL / DuckDB | pandas | polars |
|---|---|---|---|
| Select columns | `SELECT a, b FROM t` | `df[["a", "b"]]` | `df.select("a", "b")` |
| Filter rows | `WHERE amount > 20` | `df[df["amount"] > 20]` | `df.filter(pl.col("amount") > 20)` |
| AND / OR | `AND`, `OR` | `&`, `\|` (parenthesise each side) | `&`, `\|` |
| New column | `SELECT *, amount * 2 AS x` | `df.assign(x=df["amount"] * 2)` | `df.with_columns((pl.col("amount") * 2).alias("x"))` |
| Rename | `a AS b` | `df.rename(columns={"a": "b"})` | `df.rename({"a": "b"})` |
| Sort | `ORDER BY a DESC` | `df.sort_values("a", ascending=False)` | `df.sort("a", descending=True)` |
| Limit | `LIMIT 5` | `df.head(5)` | `df.head(5)` |
| Distinct | `SELECT DISTINCT a` | `df["a"].drop_duplicates()` | `df.select("a").unique()` |
| Count rows | `COUNT(*)` | `len(df)` | `df.height` |

## Aggregation and joins

| Operation | SQL / DuckDB | pandas | polars |
|---|---|---|---|
| Group + aggregate | `SELECT k, SUM(x) AS s FROM t GROUP BY k` | `df.groupby("k", as_index=False).agg(s=("x", "sum"))` | `df.group_by("k").agg(pl.col("x").sum().alias("s"))` |
| Count per group | `COUNT(*)` | `.agg(n=("x", "size"))` | `pl.len().alias("n")` |
| Inner / left join | `JOIN ... USING (k)` / `LEFT JOIN` | `a.merge(b, on="k", how="left")` | `a.join(b, on="k", how="left")` |
| Guard join keys | dbt `unique` test | `merge(..., validate="many_to_one")` | `join(..., validate="m:1")` |
| Union all | `UNION ALL` | `pd.concat([a, b], ignore_index=True)` | `pl.concat([a, b])` |

## Windows and conditionals

| Operation | SQL / DuckDB | pandas | polars |
|---|---|---|---|
| Window sum | `SUM(x) OVER (PARTITION BY k)` | `df.groupby("k")["x"].transform("sum")` | `pl.col("x").sum().over("k")` |
| Running total | `SUM(x) OVER (ORDER BY d)` | `df["x"].cumsum()` | `pl.col("x").cum_sum()` |
| Row number | `ROW_NUMBER() OVER (PARTITION BY k ORDER BY d)` | `df.groupby("k").cumcount() + 1` (after sorting) | `pl.int_range(pl.len()).over("k") + 1` (after sorting) |
| Top N per group | `QUALIFY ROW_NUMBER() OVER (...) <= n` | `df.sort_values(...).groupby("k").head(n)` | `df.sort(...).group_by("k", maintain_order=True).head(n)` |
| CASE WHEN | `CASE WHEN c THEN a ELSE b END` | `np.where(c, a, b)` or `Series.where` | `pl.when(c).then(a).otherwise(b)` |

## Cleaning and types

| Operation | SQL / DuckDB | pandas | polars |
|---|---|---|---|
| Cast | `CAST(x AS INT)` | `s.astype("int64")` | `pl.col("x").cast(pl.Int64)` |
| Safe cast | `TRY_CAST(x AS DOUBLE)` | `pd.to_numeric(s, errors="coerce")` | `pl.col("x").cast(pl.Float64, strict=False)` |
| Trim / lower | `TRIM(LOWER(x))` | `s.str.strip().str.lower()` | `pl.col("x").str.strip_chars().str.to_lowercase()` |
| Replace | `REPLACE(x, '$', '')` | `s.str.replace("$", "", regex=False)` | `pl.col("x").str.replace_all("$", "", literal=True)` |
| Parse date | `TRY_CAST(x AS DATE)` | `pd.to_datetime(s, format=..., errors="coerce")` | `pl.col("x").str.to_date("%Y-%m-%d", strict=False)` |
| Null test | `x IS NULL` | `s.isna()` | `pl.col("x").is_null()` |
| COALESCE | `COALESCE(x, 0)` | `s.fillna(0)` | `pl.col("x").fill_null(0)` |
| Dedupe by key | `QUALIFY ROW_NUMBER() OVER (PARTITION BY k ORDER BY d DESC) = 1` | `df.sort_values("d").drop_duplicates("k", keep="last")` | `df.sort("d").unique(subset="k", keep="last")` |
| Pivot | `PIVOT t ON c USING SUM(x)` | `df.pivot_table(index=, columns=, values=, aggfunc="sum")` | `df.pivot(on="c", index="k", values="x", aggregate_function="sum")` |
| Unpivot | `UNPIVOT` | `df.melt(id_vars="k")` | `df.unpivot(index="k")` |

## Reading, writing and moving between tools

| Task | Code |
|---|---|
| CSV into DuckDB | `con.execute("SELECT * FROM read_csv_auto(?)", [path])` |
| Parquet into DuckDB | `con.execute("SELECT * FROM read_parquet(?)", [path])` |
| DuckDB result to pandas / polars | `.fetchdf()` / `.pl()` |
| Query a frame with SQL | `duckdb.sql("SELECT ... FROM df")` (pandas or polars frame in scope) |
| polars to pandas | `df.to_pandas()` |
| pandas to polars | `pl.from_pandas(df)` |
| Safe SQL values | `?` / `:name` placeholders, never f-strings |

## Gotchas

- Row order is never guaranteed without an explicit sort in any of the three.
- Missing values: SQL `NULL`, pandas `NaN` / `NA`, polars `null`. pandas turns int columns with gaps into float unless you use `Int64`.
- pandas keeps an index; use `reset_index(drop=True)` before comparing frames. polars has no index.
- pandas conditions need parentheses around each comparison; polars too.
- Assign into a pandas selection with `.loc[mask, col] = value`, never a chained `df[mask][col] = value`.
