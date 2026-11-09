+++
id = "dataframes.polars-and-expressions"
title = "polars and the expression API"
minutes = 30
+++

# polars and the expression API

polars is a DataFrame library built around **expressions**: small descriptions of a column computation that polars can optimise and run in parallel. If pandas is "operate on columns one call at a time", polars is closer to "write the SELECT list and let the engine plan it", which is how you already think in SQL.

> **SQL bridge.** `pl.col("amount") * 2` is a column expression, like `amount * 2` in a `SELECT`. `df.select(...)` is the SELECT list, `with_columns` adds columns (`SELECT *, expr AS name`), `filter` is `WHERE`, `group_by().agg()` is `GROUP BY`.

## Expressions

```python
import polars as pl

orders = pl.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer_id": [10, 10, 20, 30],
    "status": ["paid", "paid", "refunded", "paid"],
    "amount": [50.0, 25.5, 80.0, 12.0],
})
print(orders.select(
    pl.col("order_id"),
    (pl.col("amount") * 1.1).round(2).alias("gross"),
))
```

`pl.col("x")` does nothing by itself, it is a *recipe*. `select` evaluates the recipes. Every expression produces a column, and `.alias` names it (`AS`).

## The verbs

| SQL | polars |
|---|---|
| `SELECT a, b` | `df.select("a", "b")` |
| `SELECT *, x * 2 AS y` | `df.with_columns((pl.col("x") * 2).alias("y"))` |
| `WHERE a > 1 AND b = 'x'` | `df.filter((pl.col("a") > 1) & (pl.col("b") == "x"))` |
| `GROUP BY k` + aggregates | `df.group_by("k").agg(...)` |
| `ORDER BY a DESC` | `df.sort("a", descending=True)` |
| `JOIN` | `df.join(other, on="k", how="left")` |
| `CASE WHEN` | `pl.when(...).then(...).otherwise(...)` |

```python
import polars as pl

orders = pl.DataFrame({
    "customer_id": [10, 10, 20, 30],
    "status": ["paid", "paid", "refunded", "paid"],
    "amount": [50.0, 25.5, 80.0, 12.0],
})
result = (
    orders
    .filter(pl.col("status") == "paid")
    .group_by("customer_id")
    .agg(
        pl.len().alias("n_orders"),
        pl.col("amount").sum().alias("total"),
    )
    .sort("total", descending=True)
)
print(result)
```

Notice there is no index anywhere. polars has no row labels, which removes a whole class of pandas surprises (`reset_index`, alignment).

## CASE WHEN

```python
import polars as pl

df = pl.DataFrame({"amount": [5.0, 60.0, 500.0]})
print(df.with_columns(
    pl.when(pl.col("amount") >= 100).then(pl.lit("large"))
      .when(pl.col("amount") >= 50).then(pl.lit("medium"))
      .otherwise(pl.lit("small"))
      .alias("tier")
))
```

`pl.lit` makes a literal; the chain mirrors `CASE WHEN ... WHEN ... ELSE ... END`.

## Window functions

`.over()` is `OVER (PARTITION BY ...)`:

```python
import polars as pl

df = pl.DataFrame({"region": ["e", "e", "w"], "amount": [10, 30, 5]})
print(df.with_columns(
    pl.col("amount").sum().over("region").alias("region_total"),
    pl.col("amount").rank("ordinal", descending=True).over("region").alias("rk"),
))
```

## Lazy frames

An eager DataFrame runs each step immediately. A **LazyFrame** records the steps and runs them when you call `collect()`, so polars can reorder them: push filters before joins, read only the columns you use, stream big files.

```python
import polars as pl, tempfile, pathlib

p = pathlib.Path(tempfile.mkdtemp()) / "x.csv"
p.write_text("k,v\na,1\na,2\nb,5\n")

lazy = (
    pl.scan_csv(p)                     # nothing is read yet
    .filter(pl.col("v") > 1)
    .group_by("k")
    .agg(pl.col("v").sum())
    .sort("k")
)
print(lazy.collect())
```

`scan_csv` / `scan_parquet` are the entry points for files bigger than comfortable memory. This is the same idea as a SQL optimiser: you describe, the engine plans.

## polars, pandas, DuckDB: a first rule of thumb

- You already write excellent SQL and the data is in files: **DuckDB**.
- You need the ecosystem (plotting, scikit-learn, a library that takes a pandas frame): **pandas**.
- You are building a Python pipeline with heavier transforms, want speed and clear expressions: **polars**.

The last lesson of this module turns that into a decision guide.

## Common mistakes

- Using Python's `and`/`or` between expressions raises `TypeError: the truth value of an Expr is ambiguous`. Use `&`, `|` and parentheses.
- `ColumnNotFoundError: amout` typo, same as pandas' `KeyError`.
- Forgetting to alias: `pl.col("a") + pl.col("b")` is named `a`. Give computed columns real names.
- `SchemaError` / `ComputeError` from mixing types: polars is strict. `pl.col("x").cast(pl.Float64)` is your explicit `CAST`.
- Calling `.collect()` too early on a lazy frame: you lose the optimisation and may load everything.
- Expecting group order: `group_by` does not sort keys. Add `.sort(...)` for deterministic output.

## What to take away

1. polars works with expressions: `pl.col(...)` recipes inside `select`, `with_columns`, `filter` and `agg`.
2. The verbs map directly to SQL; `when/then/otherwise` is `CASE WHEN` and `.over()` is a window.
3. No index, strict types, explicit `cast`.
4. Lazy frames plan the whole query; `scan_*` plus `collect()` handles big files.
5. Sort before comparing group results; `group_by` order is not a contract.
