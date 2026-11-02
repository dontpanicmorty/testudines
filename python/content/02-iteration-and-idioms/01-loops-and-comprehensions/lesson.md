+++
id = "iteration-and-idioms.loops-and-comprehensions"
title = "Loops and comprehensions"
minutes = 30
+++

# Loops and comprehensions

SQL is declarative: you describe the result set. Python gives you the procedural version, a loop that visits each row, plus a compact declarative-feeling syntax, the **comprehension**, that covers most of what you'd write `SELECT … WHERE` for.

> **SQL bridge.** `SELECT f(x) FROM t WHERE p(x)` → `[f(x) for x in t if p(x)]`. `SELECT DISTINCT` → a set comprehension. A join on position → `zip`. `ROW_NUMBER()` → `enumerate`.

## for loops

```python
for region in ["EU", "US", "APAC"]:
    print(region)
```

A `for` loop works on anything iterable: lists, tuples, strings, dict keys, files, `range`.

```python
for ch in "abc":
    print(ch)

for i in range(3):         # 0, 1, 2 (stop excluded)
    print(i)

print(list(range(2, 10, 3)))   # start, stop, step
```

Python programmers rarely loop with an index. If you write `for i in range(len(xs))`, there is almost always a better way.

## enumerate and zip

Need the position too? `enumerate`. Need to walk two lists together? `zip`.

```python
names = ["ada", "grace", "linus"]

for i, name in enumerate(names, start=1):
    print(i, name)

amounts = [50, 20, 90]
for name, amount in zip(names, amounts):
    print(name, amount)

print(dict(zip(names, amounts)))
```

`zip` stops at the shortest input. Spotting silent truncation is a data-quality skill: use `zip(a, b, strict=True)` to raise if lengths differ.

## while and break

`while` repeats until a condition fails, useful when you don't know how many iterations you need (retry loops, pagination).

```python
page = 1
while page <= 3:
    print("fetching page", page)
    page += 1

for n in [3, 8, 12, 5]:
    if n > 10:
        print("found", n)
        break
else:
    print("none over 10")   # runs only if the loop never hit break
```

`continue` skips to the next iteration. Forgetting to update the variable in a `while` loop gives an infinite loop.

## Naive loop to list comprehension

The naive way to transform and filter:

```python
orders = [
    {"id": 1, "status": "paid", "amount": 50.0},
    {"id": 2, "status": "refunded", "amount": 20.0},
    {"id": 3, "status": "paid", "amount": 90.0},
]

big_ids = []
for o in orders:
    if o["amount"] > 30:
        big_ids.append(o["id"])
print(big_ids)
```

The idiom, read as `SELECT id FROM orders WHERE amount > 30`:

```python
orders = [
    {"id": 1, "status": "paid", "amount": 50.0},
    {"id": 2, "status": "refunded", "amount": 20.0},
    {"id": 3, "status": "paid", "amount": 90.0},
]

big_ids = [o["id"] for o in orders if o["amount"] > 30]
print(big_ids)
```

The shape is `[expression for item in iterable if condition]`: the `for` part is `FROM`, the `if` part is `WHERE`, the leading expression is `SELECT`. A transform without a filter just drops the `if`.

```python
orders = [
    {"id": 1, "status": "paid", "amount": 50.0},
    {"id": 2, "status": "refunded", "amount": 20.0},
    {"id": 3, "status": "paid", "amount": 90.0},
]

amounts = [o["amount"] for o in orders]
with_tax = [round(a * 1.2, 2) for a in amounts]
print(with_tax)
```

A conditional **inside** the expression is a `CASE`, and goes before the `for`:

```python
orders = [
    {"id": 1, "status": "paid", "amount": 50.0},
    {"id": 2, "status": "refunded", "amount": 20.0},
    {"id": 3, "status": "paid", "amount": 90.0},
]

labels = ["big" if o["amount"] > 30 else "small" for o in orders]
print(labels)
```

> **Predict first.** What is the difference between `[x for x in xs if x > 0]` and `[x if x > 0 else 0 for x in xs]`? The first **drops** negatives (shorter list); the second **replaces** them (same length).

## Dict and set comprehensions

```python
orders = [
    {"id": 1, "status": "paid", "amount": 50.0},
    {"id": 2, "status": "refunded", "amount": 20.0},
    {"id": 3, "status": "paid", "amount": 90.0},
]

by_id = {o["id"]: o for o in orders}               # index rows by key
print(sorted(by_id))

status_set = {o["status"] for o in orders}         # SELECT DISTINCT
print(sorted(status_set))

paid_totals = {o["id"]: o["amount"] for o in orders if o["status"] == "paid"}
print(paid_totals)
```

`{k: v for ...}` builds a dict; `{x for ...}` builds a set. Dict comprehensions are the idiomatic "build a lookup table" tool: one pass, then O(1) lookups, as opposed to scanning a list for every row.

Nested loops work too, read left to right like the nested `for` statements:

```python
pairs = [(r, p) for r in ["EU", "US"] for p in ["free", "pro"]]
print(pairs)
```

## When not to use a comprehension

If it needs more than one `if`, nested logic, or side effects such as printing or appending elsewhere, use a normal loop. A comprehension should fit on a line or two and read like one sentence.

## Common mistakes

```python
orders = [
    {"id": 1, "status": "paid", "amount": 50.0},
    {"id": 2, "status": "refunded", "amount": 20.0},
    {"id": 3, "status": "paid", "amount": 90.0},
]

total = 0
for o in orders:
    total += o["amount"]
print(total)
```

That's fine, but `sum(o["amount"] for o in orders)` is the idiom. Others:

- Using a comprehension for side effects: `[print(x) for x in xs]` builds a pointless list.
- `TypeError: 'int' object is not iterable`: you wrote `for x in 5` when you meant `for x in range(5)`.
- `ValueError: zip() argument 2 is shorter than argument 1` with `strict=True`: the inputs really do differ in length; that is the check working.
- Reusing the loop variable name after the loop and being surprised by its leftover value.
- Changing a list while iterating over it; build a new one instead.

## What to take away

1. Loop over things directly; use `enumerate` for positions and `zip` to pair sequences.
2. `[expr for x in xs if cond]` is `SELECT expr … WHERE cond`.
3. A conditional expression inside gives `CASE`; a trailing `if` gives `WHERE`.
4. Dict/set comprehensions build lookup tables and `DISTINCT` sets.
5. If a comprehension needs more than a line or two, write a loop.
