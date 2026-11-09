+++
id = "wrangling-in-pure-python.joins-and-aggregations-by-hand"
title = "Joins and aggregations by hand"
minutes = 35
+++

# Joins and aggregations by hand

You have written thousands of `JOIN`s and `GROUP BY`s. Doing them once in plain Python is the fastest way to understand what the engine does, and it is the tool you reach for when the data is a list of dicts from an API, not a table. (When data is large and tabular you will use duckdb or polars; the mental model is the same.)

> **SQL bridge.** A **hash join** builds a lookup on one side (`dict` keyed by the join key) and probes it with each row from the other side. That is literally what a warehouse does for an equi-join.

Sample data used below:

```python
customers = [
    {"customer_id": 1, "name": "Ada", "region": "EU"},
    {"customer_id": 2, "name": "Bo", "region": "US"},
    {"customer_id": 3, "name": "Cy", "region": "EU"},
]
orders = [
    {"order_id": 10, "customer_id": 1, "amount": 50},
    {"order_id": 11, "customer_id": 1, "amount": 70},
    {"order_id": 12, "customer_id": 2, "amount": 20},
    {"order_id": 13, "customer_id": 9, "amount": 99},   # no such customer
]
print(len(customers), len(orders))
```

## Inner join

```sql
SELECT o.order_id, c.name, o.amount
FROM orders o JOIN customers c USING (customer_id)
```

```python
customers = [{"customer_id": 1, "name": "Ada"}, {"customer_id": 2, "name": "Bo"}]
orders = [
    {"order_id": 10, "customer_id": 1, "amount": 50},
    {"order_id": 12, "customer_id": 2, "amount": 20},
    {"order_id": 13, "customer_id": 9, "amount": 99},
]

by_id = {c["customer_id"]: c for c in customers}      # build side
joined = []
for o in orders:                                       # probe side
    c = by_id.get(o["customer_id"])
    if c is not None:
        joined.append({"order_id": o["order_id"], "name": c["name"], "amount": o["amount"]})
print(joined)
```

Build the dict from the **smaller** side. Lookup is constant time, so the whole join is one pass over each side. The naive alternative, a nested loop scanning `customers` for every order, is quadratic and gets painfully slow.

## Left join semantics

A `LEFT JOIN` keeps every left row. Unmatched ones get `NULL` (`None`) for the right columns.

```python
customers = [{"customer_id": 1, "name": "Ada"}, {"customer_id": 3, "name": "Cy"}]
orders = [{"order_id": 10, "customer_id": 1, "amount": 50}]

orders_by_cust = {}
for o in orders:
    orders_by_cust.setdefault(o["customer_id"], []).append(o)

result = []
for c in customers:
    matches = orders_by_cust.get(c["customer_id"], [])
    if matches:
        for o in matches:                 # one output row per match (fan-out)
            result.append({**c, "order_id": o["order_id"], "amount": o["amount"]})
    else:
        result.append({**c, "order_id": None, "amount": None})
print(result)
```

Two rules to remember, the same as in SQL:

1. A left row with no match is kept, with `None`s.
2. A left row with **several** matches is repeated once per match. Joining on a non-unique key silently multiplies rows and inflates sums. Check key uniqueness on the side you expect to be unique.

## Group and aggregate

```sql
SELECT region, COUNT(*), SUM(amount) FROM ... GROUP BY region
```

```python
from collections import defaultdict

rows = [
    {"region": "EU", "amount": 50},
    {"region": "US", "amount": 20},
    {"region": "EU", "amount": 70},
]

totals = defaultdict(lambda: {"n": 0, "sum": 0})
for r in rows:
    g = totals[r["region"]]
    g["n"] += 1
    g["sum"] += r["amount"]

for region in sorted(totals):
    g = totals[region]
    print(region, g["n"], g["sum"], g["sum"] / g["n"])
```

`defaultdict` creates the missing group on first touch, so the loop has no "if key not in dict" clutter. `collections.Counter` is a ready-made `COUNT(*) ... GROUP BY`:

```python
from collections import Counter

statuses = ["paid", "open", "paid", "void", "paid"]
print(Counter(statuses).most_common())
```

For "group by" over rows **already sorted** by key you can stream with `itertools.groupby`, but it only groups *adjacent* equal keys, so sort first (a classic trap). The dict approach does not need sorting.

## Running totals and window functions

```sql
SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date
                  ROWS UNBOUNDED PRECEDING) AS running_total,
LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount
```

A window function is "partition, order, then carry state along each partition". In Python that is: group, sort each group, loop with a running variable.

```python
from itertools import groupby

orders = [
    {"customer": "Ada", "day": "2025-06-02", "amount": 70},
    {"customer": "Bo", "day": "2025-06-01", "amount": 20},
    {"customer": "Ada", "day": "2025-06-01", "amount": 50},
    {"customer": "Ada", "day": "2025-06-09", "amount": 10},
]

ordered = sorted(orders, key=lambda r: (r["customer"], r["day"]))    # PARTITION BY, ORDER BY
out = []
for customer, group in groupby(ordered, key=lambda r: r["customer"]):
    running, prev = 0, None
    for r in group:
        running += r["amount"]
        out.append({**r, "running_total": running, "prev_amount": prev})
        prev = r["amount"]

for r in out:
    print(r["customer"], r["day"], r["amount"], r["running_total"], r["prev_amount"])
```

Here the sort is exactly what makes `groupby` safe. Notice that `running` and `prev` reset per partition. That reset is the `PARTITION BY`.

## Checking your work

A hand-written join is only trustworthy if you check it against an invariant, the same as a dbt test:

```python
orders = [{"id": 1, "cid": 1}, {"id": 2, "cid": 9}]
customers = [{"cid": 1}]
known = {c["cid"] for c in customers}
orphans = [o["id"] for o in orders if o["cid"] not in known]
print("orders with no customer:", orphans)    # a relationships test
```

Row counts: after a left join on a unique key, `len(result) == len(left)`. After an inner join it is at most that.

## Common mistakes

- Building the lookup from the wrong side and then losing rows.
- A dict keyed by a non-unique column: later rows silently overwrite earlier ones. Use `setdefault(key, [])` when the key can repeat.
- Joining `int` ids with `str` ids (`1` vs `"1"` never match). CSV ids are strings; convert one side.
- `itertools.groupby` without sorting, giving the same key several times.
- Mutating dicts shared between result rows. Build new dicts: `{**c, "x": 1}`.

## What to take away

1. Hash join: dict on one side, probe with the other.
2. Left join keeps unmatched left rows with `None`, and repeats a left row per match.
3. Aggregate with `defaultdict` or `Counter`; one pass, no sorting needed.
4. Window-style calculations are group, sort, then carry state per group.
5. Always check join key types and uniqueness, and compare row counts.
