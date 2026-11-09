+++
id = "dataframes.pandas-essentials"
title = "pandas essentials, next to the SQL"
minutes = 30
+++

# pandas essentials, next to the SQL

A pandas **DataFrame** is a table held in memory: named columns, each with a type, plus an index. Everything you do in `SELECT ... FROM ... WHERE ... GROUP BY ... JOIN` has a pandas spelling. This lesson shows each one next to the SQL so you can translate in your head instead of memorising.

> **SQL bridge.** Series = a column. DataFrame = a table. Index = a row label (you will mostly ignore it and call `reset_index`).

## Build a DataFrame

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer_id": [10, 10, 20, 30],
    "status": ["paid", "paid", "refunded", "paid"],
    "amount": [50.0, 25.5, 80.0, 12.0],
})
print(orders)
print(orders["amount"].sum())
```

`orders["amount"]` is a Series. Vectorised operations act on the whole column at once, there is no loop: `orders["amount"] * 2`.

## Reading files: say what the types are

`read_csv` guesses types. Guesses go wrong on IDs with leading zeros, mixed columns and dates. Be explicit:

```python
import io
import pandas as pd

csv = io.StringIO("sku,qty,shipped\n007,3,2025-01-05\n010,5,2025-01-09\n")
df = pd.read_csv(csv, dtype={"sku": "string"}, parse_dates=["shipped"])
print(df)
print(df["sku"].tolist(), df["shipped"].dt.year.tolist())
```

Without the `dtype`, `007` would be read as the integer `7` and the leading zeros would be gone. In SQL you would declare `sku VARCHAR` in the table definition; this is the same decision.

## SELECT, WHERE, computed columns

| SQL | pandas |
|---|---|
| `SELECT order_id, amount` | `df[["order_id", "amount"]]` |
| `WHERE status = 'paid'` | `df[df["status"] == "paid"]` |
| `WHERE status = 'paid' AND amount > 20` | `df[(df["status"] == "paid") & (df["amount"] > 20)]` |
| `amount * 1.1 AS gross` | `df.assign(gross=df["amount"] * 1.1)` |
| `ORDER BY amount DESC` | `df.sort_values("amount", ascending=False)` |
| `LIMIT 2` | `df.head(2)` |

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "status": ["paid", "paid", "refunded", "paid"],
    "amount": [50.0, 25.5, 80.0, 12.0],
})
big_paid = orders[(orders["status"] == "paid") & (orders["amount"] > 20)]
print(big_paid)
print(orders.assign(gross=orders["amount"] * 1.1).sort_values("amount", ascending=False).head(2))
```

Two things trip SQL people. Conditions are combined with `&` and `|` (not `and`/`or`), and **each condition needs parentheses** because `&` binds tighter than `>`. And `assign` returns a *new* frame; the original is untouched.

> **Predict first.** `orders["amount"] > 20` is not a list of rows. What is it?

It is a Series of booleans, one per row. Indexing a DataFrame with it keeps the `True` rows. That is exactly what `WHERE` evaluates.

## GROUP BY

```python
import pandas as pd

orders = pd.DataFrame({
    "customer_id": [10, 10, 20, 30],
    "status": ["paid", "paid", "refunded", "paid"],
    "amount": [50.0, 25.5, 80.0, 12.0],
})
summary = (
    orders.groupby("customer_id", as_index=False)
    .agg(n_orders=("amount", "count"), total=("amount", "sum"), biggest=("amount", "max"))
)
print(summary)
```

```sql
SELECT customer_id, COUNT(amount) AS n_orders, SUM(amount) AS total, MAX(amount) AS biggest
FROM orders GROUP BY customer_id
```

The named-aggregation form `new_name=("column", "func")` is the readable one; it maps one-to-one onto `AS`. `as_index=False` keeps the group key as a normal column (otherwise it becomes the index). Pandas omits the `ORDER BY`: group keys come out sorted by default, but say so explicitly with `sort_values` when it matters.

## JOIN

```python
import pandas as pd

orders = pd.DataFrame({"order_id": [1, 2, 3], "customer_id": [10, 20, 99]})
customers = pd.DataFrame({"customer_id": [10, 20, 30], "name": ["Ada", "Linus", "Tim"]})

print(orders.merge(customers, on="customer_id", how="left"))
print(orders.merge(customers, on="customer_id", how="inner"))
```

`merge` is `JOIN`: `how` is `inner`, `left`, `right` or `outer`. Unmatched rows get `NaN`, pandas' missing marker, where SQL would show `NULL`. Join explosions happen here exactly as in SQL: if the right side has duplicate keys, rows multiply. Guard with `validate="many_to_one"` and pandas raises instead of silently duplicating:

```python
import pandas as pd

left = pd.DataFrame({"k": [1, 2]})
right = pd.DataFrame({"k": [1, 1], "v": ["a", "b"]})   # duplicate key
try:
    left.merge(right, on="k", validate="many_to_one")
except pd.errors.MergeError as exc:
    print("MergeError:", exc)
```

That is a `unique` test in dbt, applied at the moment it matters.

## Common mistakes

- `ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().` You used `and`/`or` or an `if` on a whole column. Use `&`, `|` and parentheses.
- `KeyError: 'amout'` a typo in a column name. Print `df.columns` first.
- Expecting `df.sort_values(...)` or `df.assign(...)` to change `df`. They return new frames; assign the result.
- `groupby` result has the key as the index and you cannot find the column. Add `as_index=False` or call `.reset_index()`.
- Row order after `merge` or `groupby` is not a contract. Sort before comparing or exporting.

## What to take away

1. Series is a column, DataFrame a table; operations are vectorised, not looped.
2. State dtypes when reading files (`dtype=`, `parse_dates=`).
3. `WHERE` is a boolean mask; combine with `&`, `|` and parentheses.
4. `groupby(...).agg(name=("col", "func"))` is `GROUP BY` with `AS`.
5. `merge` is `JOIN`; use `validate=` to catch key duplication like a dbt test.
