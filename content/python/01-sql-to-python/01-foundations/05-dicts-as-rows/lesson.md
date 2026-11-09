+++
id = "foundations.dicts-as-rows"
title = "Dicts as rows"
minutes = 30
+++

# Dicts as rows

A **dict** maps keys to values. For a data engineer it is the natural shape of one **row**: column name → cell. A **list of dicts** is a table, and it is exactly what JSON APIs hand you. Most Python data work, before pandas or polars enter the picture, is dict and list manipulation.

> **SQL bridge.** A row → `{"id": 1, "plan": "pro"}`. A result set → `[{...}, {...}]`. `SELECT col` → `row["col"]`. `COALESCE(col, 'x')` → `row.get("col", "x")`. `JSON:path` → nested indexing.

## Creating and reading

```python
customer = {"id": 1, "name": "Ada", "plan": "pro", "email": None}

print(customer["name"])
print(len(customer))
print("plan" in customer)     # tests KEYS
print(customer.keys())
print(list(customer.values()))
```

Missing key:

```python
# no-run
customer = {"id": 1}
print(customer["plan"])
```

```text
KeyError: 'plan'
```

## .get: your COALESCE

```python
customer = {"id": 1, "name": "Ada"}
print(customer.get("plan"))             # None, no error
print(customer.get("plan", "free"))     # default
```

Use `[]` when the key **must** exist (a missing one is a bug and the `KeyError` is good news); use `.get` when it is optional. Beware: `.get("k", d)` only substitutes for a **missing** key. A key that is present with value `None` returns `None`:

```python
row = {"plan": None}
print(row.get("plan", "free"))
print(row.get("plan") or "free")
```

## Adding, changing, removing

```python
row = {"id": 1}
row["plan"] = "pro"            # add
row["plan"] = "team"           # change
row.update({"region": "EU", "active": True})
removed = row.pop("active")    # remove and return
del row["region"]
print(row, removed)
```

## Iterating

```python
row = {"id": 1, "plan": "pro", "region": "EU"}

for key in row:
    print(key)

for key, value in row.items():
    print(f"{key} = {value}")
```

Iterating a dict yields keys. Use `.items()` for key and value together; dicts remember insertion order.

## Nested dicts

Event payloads nest. Walk them one level at a time:

```python
event = {"user": {"id": 7, "geo": {"country": "DE"}}, "props": {"plan": "pro"}}

print(event["user"]["geo"]["country"])
print(event.get("props", {}).get("plan"))
print(event.get("device", {}).get("os", "unknown"))   # safe chain
```

`.get(key, {})` returns an empty dict when the level is missing, so the next `.get` is safe. A bare `event["device"]["os"]` would raise `KeyError`.

## A list of dicts is a table

```python
orders = [
    {"id": 1, "customer": "ada", "amount": 50.0},
    {"id": 2, "customer": "grace", "amount": 20.0},
    {"id": 3, "customer": "ada", "amount": 30.0},
]

print(orders[0]["customer"])                         # first row, one column
print([o["amount"] for o in orders])                 # SELECT amount
print([o for o in orders if o["amount"] > 25])       # WHERE amount > 25
print(sum(o["amount"] for o in orders))              # SUM(amount)
print(max(orders, key=lambda o: o["amount"])["id"])  # row with MAX(amount)
```

## Merging

```python
defaults = {"retries": 3, "timeout": 30}
overrides = {"timeout": 5}

config = {**defaults, **overrides}     # later wins
print(config)
print(defaults | overrides)            # same, Python 3.9+
```

Both create a **new** dict. `defaults.update(overrides)` changes `defaults` in place, so reach for it only when you mean to. Merging is how configs layer and how you "enrich" a row: `{**row, "region": lookup[row["customer"]]}`.

## Counting and grouping by hand

The pattern you will write a hundred times: tally per key.

```python
orders = [
    {"customer": "ada", "amount": 50.0},
    {"customer": "grace", "amount": 20.0},
    {"customer": "ada", "amount": 30.0},
]

totals = {}
for o in orders:
    totals[o["customer"]] = totals.get(o["customer"], 0) + o["amount"]
print(totals)
```

That is `SELECT customer, SUM(amount) … GROUP BY customer`. (The next module shows nicer tools, `Counter` and `defaultdict`, for the same job.)

Grouping rows into lists:

```python
orders = [
    {"customer": "ada", "amount": 50.0},
    {"customer": "grace", "amount": 20.0},
    {"customer": "ada", "amount": 30.0},
]

by_customer = {}
for o in orders:
    by_customer.setdefault(o["customer"], []).append(o)
print({k: len(v) for k, v in by_customer.items()})
```

Keys must be **hashable** (immutable): strings, numbers and tuples work, lists don't.

## Common mistakes

- `KeyError: 'plan'`: the key is missing. Decide whether that is a bug (use `[]`) or normal (use `.get`).
- `TypeError: unhashable type: 'list'`: you used a list as a key; use a tuple.
- Mutating a dict while iterating it: `RuntimeError: dictionary changed size during iteration`. Iterate over `list(d)` or build a new dict.
- Assuming `.get(k, default)` replaces `None` values; it only fills **missing** keys.
- `b = a` on a dict aliases it, just like lists. Use `dict(a)` or `a.copy()`.

## What to take away

1. A dict is a row; a list of dicts is a table.
2. `d[k]` for required keys, `d.get(k, default)` for optional ones (missing, not `None`).
3. Walk nested data with chained `.get(k, {})`.
4. Merge with `{**a, **b}`; later keys win and the inputs are untouched.
5. Count and group with `d[k] = d.get(k, 0) + 1` and `setdefault(k, []).append(...)`.
