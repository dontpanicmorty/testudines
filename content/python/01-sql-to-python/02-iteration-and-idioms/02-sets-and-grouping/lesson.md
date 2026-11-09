+++
id = "iteration-and-idioms.sets-and-grouping"
title = "Sets and grouping"
minutes = 30
+++

# Sets and grouping

Two of the most common data tasks, "which values appear" and "aggregate by key", have dedicated tools in Python. Sets give you `DISTINCT` and the set operators; `Counter` and `defaultdict` give you `GROUP BY`.

> **SQL bridge.** `SELECT DISTINCT` → `set(...)`. `UNION / INTERSECT / EXCEPT` → `| & -`. `COUNT(*) GROUP BY k` → `Counter`. `ARRAY_AGG … GROUP BY k` → `defaultdict(list)`. `ORDER BY` → `sorted(key=...)`.

## Sets

A set is an unordered collection of **unique, hashable** values. Membership tests are fast, the reason to prefer a set over a list when you are asking "is x in there?" thousands of times.

```python
emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]
unique = set(emails)
print(len(emails), len(unique))
print("a@x.com" in unique)
print(sorted(unique))      # sets have no order; sort to display
```

Adding and removing:

```python
s = {"eu", "us"}
s.add("apac")
s.add("eu")          # no effect, already there
s.discard("us")      # no error if missing (remove() raises KeyError)
print(sorted(s))
```

Careful: `{}` is an **empty dict**, not an empty set. Use `set()`.

```python
print(type({}), type(set()))
```

## Set algebra = UNION / INTERSECT / EXCEPT

```python
yesterday = {"c1", "c2", "c3"}
today = {"c2", "c3", "c4"}

print(sorted(yesterday | today))   # UNION       -> all customers seen
print(sorted(yesterday & today))   # INTERSECT   -> in both
print(sorted(today - yesterday))   # EXCEPT      -> new today
print(sorted(yesterday - today))   # churned
print(sorted(yesterday ^ today))   # in exactly one of them
```

This is the cleanest way to diff two key lists, for example "which ids are in the source but missing from the target table", the heart of reconciliation checks.

```python
source_ids = {1, 2, 3, 4}
loaded_ids = {1, 2, 4}
missing = source_ids - loaded_ids
print(missing)
print(source_ids.issubset(loaded_ids), {1, 2} <= loaded_ids)
```

Unlike SQL, `UNION` in Python is always the de-duplicating one. For `UNION ALL`, concatenate lists: `a + b`.

## Counter: COUNT(*) GROUP BY

The manual tally from the dict lesson works, but `collections.Counter` is built for it.

```python
from collections import Counter

statuses = ["paid", "paid", "refunded", "paid", "pending", "refunded"]
counts = Counter(statuses)
print(counts)
print(counts["paid"], counts["nope"])    # missing key -> 0, no KeyError
print(counts.most_common(2))
```

`most_common(n)` is `ORDER BY count DESC LIMIT n`. You can also feed it a generator: `Counter(row["region"] for row in rows)`.

## defaultdict: group into lists, sums, sets

A `defaultdict` creates a missing value automatically the first time you touch a key. Pass the factory: `list`, `int`, `set`.

```python
from collections import defaultdict

orders = [
    {"customer": "ada", "amount": 50.0},
    {"customer": "grace", "amount": 20.0},
    {"customer": "ada", "amount": 30.0},
]

by_customer = defaultdict(list)       # ARRAY_AGG
totals = defaultdict(float)           # SUM
for o in orders:
    by_customer[o["customer"]].append(o["amount"])
    totals[o["customer"]] += o["amount"]

print(dict(by_customer))
print(dict(totals))
```

Compare with the dict version from last lesson: no `.get(k, 0)` and no `setdefault`. One trap: **reading** a missing key on a `defaultdict` creates it, so `d["typo"]` quietly adds an entry. Convert to a plain `dict(...)` when you hand the result onward.

## GROUP BY with several aggregates

When you need count, sum and max at once, group the rows first and then aggregate each group:

```python
from collections import defaultdict

orders = [
    {"customer": "ada", "amount": 50.0},
    {"customer": "grace", "amount": 20.0},
    {"customer": "ada", "amount": 30.0},
]

groups = defaultdict(list)
for o in orders:
    groups[o["customer"]].append(o["amount"])

summary = {
    cust: {"n": len(vals), "sum": sum(vals), "max": max(vals)}
    for cust, vals in groups.items()
}
print(summary)
```

A tuple works as a composite key: `groups[(o["region"], o["plan"])]` is `GROUP BY region, plan`.

## sorted with key: ORDER BY

```python
rows = [("ada", 80), ("grace", 95), ("linus", 80)]

print(sorted(rows, key=lambda r: r[1], reverse=True))
print(sorted(rows, key=lambda r: (-r[1], r[0])))   # score DESC, name ASC
```

A tuple key sorts by the first element, then the second, and so on. Negating a number flips its direction; for strings, use two passes (sort by the secondary key first, then the primary, since the sort is stable). `operator.itemgetter(1)` is a faster equivalent of `lambda r: r[1]`.

```python
from operator import itemgetter

rows = [("ada", 80), ("grace", 95), ("linus", 80)]
print(sorted(rows, key=itemgetter(1)))
```

## Common mistakes

- `TypeError: unhashable type: 'dict'` (or `'list'`): sets and dict keys need hashable items. Convert to a tuple, e.g. `tuple(sorted(d.items()))`.
- `s = {}` then `s.add(1)` gives `AttributeError: 'dict' object has no attribute 'add'`.
- Expecting set order: sets are unordered, so don't index them (`TypeError: 'set' object is not subscriptable`).
- Forgetting that `Counter` treats the **elements** of what you pass; `Counter("paid")` counts letters.
- Using `.sort()` on a list of dicts without `key=`: `TypeError: '<' not supported between instances of 'dict' and 'dict'`.

## What to take away

1. A set is `DISTINCT` with fast membership; `|`, `&`, `-` are `UNION`, `INTERSECT`, `EXCEPT`.
2. Diff key sets to find what is missing or new.
3. `Counter` for counts, `most_common(n)` for top-N.
4. `defaultdict(list/int/float)` for `GROUP BY`; tuple keys for multiple columns.
5. `sorted(..., key=...)` with tuple keys is a multi-column `ORDER BY`.
