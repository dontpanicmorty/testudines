+++
id = "foundations.lists-and-tuples"
title = "Lists and tuples"
minutes = 30
+++

# Lists and tuples

A **list** is an ordered, changeable sequence: think of one column's values, or an `ARRAY`. A **tuple** is the same shape but fixed once made, which makes it ideal for a single record like `(id, name)`.

> **SQL bridge.** `ARRAY_AGG(col)` → a list. `ORDER BY x LIMIT 3` → `sorted(...)[:3]`. A row from a cursor → a tuple.

## Creating and indexing

```python
amounts = [120.0, 35.5, 99.9, 10.0]

print(amounts[0])     # first (indexes start at 0)
print(amounts[-1])    # last
print(len(amounts))
print(35.5 in amounts)
```

Out-of-range reads fail loudly:

```python
# no-run
amounts = [1, 2, 3]
print(amounts[3])
```

```text
IndexError: list index out of range
```

## Slicing

`seq[start:stop:step]`: start included, stop **excluded**, every part optional. A slice always returns a new list.

```python
xs = [10, 20, 30, 40, 50]
print(xs[1:3])    # [20, 30]
print(xs[:2])     # first two
print(xs[-2:])    # last two
print(xs[::2])    # every other
print(xs[::-1])   # reversed copy
```

Because `stop` is excluded, `xs[:k] + xs[k:]` is always the whole list, with no overlap.

## Mutating a list

```python
cart = ["pen"]
cart.append("book")          # add one
cart.extend(["bag", "cup"])  # add many
cart.insert(0, "lamp")
cart.remove("pen")           # first matching value
last = cart.pop()            # remove and return last
print(cart, last)
```

> **Predict first.** `append` versus `extend` with a list argument:

```python
a = [1, 2]
a.append([3, 4])
b = [1, 2]
b.extend([3, 4])
print(a)
print(b)
```

`append` adds the list as **one element**: `[1, 2, [3, 4]]`. `extend` adds each item: `[1, 2, 3, 4]`.

Mutating methods like `append`, `sort` and `reverse` return `None`, so `xs = xs.sort()` throws your list away. A tell-tale bug.

## Sorting

```python
xs = [3, 1, 2]
print(sorted(xs))                # new list; xs unchanged
print(sorted(xs, reverse=True))
xs.sort()                        # in place; returns None
print(xs)

orders = [("o1", 50), ("o2", 20), ("o3", 90)]
print(sorted(orders, key=lambda o: o[1]))   # ORDER BY amount
```

`key=` is a function applied to each item to get the sort value, the equivalent of the expression in `ORDER BY`. Sorting is stable, so you can sort by a secondary key first, then the primary.

## Tuples and unpacking

```python
point = (3, 4)
x, y = point
print(x, y)

first, *rest = [1, 2, 3, 4]
print(first, rest)

a, b = 1, 2
a, b = b, a       # swap without a temp
print(a, b)

for order_id, amount in [("o1", 50), ("o2", 20)]:
    print(order_id, amount)
```

Tuples can't be changed (`point[0] = 9` raises `TypeError: 'tuple' object does not support item assignment`), so they are safe as dictionary keys and for "this is one thing" groupings. A one-element tuple needs a trailing comma: `(5,)`.

## The aliasing trap

`b = a` does **not** copy a list. It attaches a second name to the same list.

> **Predict first.** What does `a` hold after this?

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

`[1, 2, 3, 4]`: one list, two names. To make a real (shallow) copy:

```python
a = [1, 2, 3]
b = a.copy()      # or list(a), or a[:]
b.append(4)
print(a, b)
```

Shallow means nested lists are still shared:

```python
grid = [[0, 0], [0, 0]]
copy = grid.copy()
copy[0][0] = 9
print(grid)
```

A classic related bug is `[[0] * 2] * 2`, which builds two references to the same inner list; use `[[0] * 2 for _ in range(2)]`.

## Common mistakes

- `IndexError: list index out of range`: the last valid index is `len(xs) - 1`; check for empty lists.
- `AttributeError: 'NoneType' object has no attribute 'append'`: you wrote `xs = xs.sort()` or similar, and `xs` is now `None`.
- `ValueError: list.remove(x): x not in list`: test with `in` first.
- `ValueError: not enough values to unpack (expected 3, got 2)`: unpacking shape mismatch.
- Modifying a list while looping over it skips items; build a new list instead.

## What to take away

1. Indexes start at 0, negatives count from the end, slices exclude the stop.
2. `append` adds one item, `extend` adds many; mutating methods return `None`.
3. `sorted(xs, key=...)` is your `ORDER BY`.
4. Tuples are fixed records; unpack them: `a, b = pair`.
5. `b = a` aliases. Copy with `.copy()` when you need an independent list.
