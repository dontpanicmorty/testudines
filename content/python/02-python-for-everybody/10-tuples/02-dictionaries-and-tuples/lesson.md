+++
id = "everybody.tuples.dictionaries-and-tuples"
title = "Dictionaries and tuples"
minutes = 25
+++

# Dictionaries and tuples

Dictionaries and tuples fit together neatly. A dictionary can hand you its contents as tuples, and a tuple can serve as a dictionary key. This lesson shows both.

## `.items()` gives pairs

The `.items()` method returns every key/value pair of a dictionary as a two-item tuple.

```python
prices = {"tea": 3, "milk": 2, "rice": 5}
print(list(prices.items()))
# [('tea', 3), ('milk', 2), ('rice', 5)]
```

(Wrapping with `list(...)` is just for printing. You can loop over `.items()` directly.)

Because each pair is a tuple, we can unpack it with tuple assignment right in the `for` line.

```python
for item, price in prices.items():
    print(item, "costs", price)
```

On each trip around the loop, Python takes the next pair and does `item, price = pair` for you. This is called **multiple assignment in a loop**, and it reads much better than `prices[item]`.

## Building a dictionary from pairs

Going the other way, `dict()` accepts a list of pairs.

```python
pairs = [("a", 1), ("b", 2)]
d = dict(pairs)
print(d)    # {'a': 1, 'b': 2}
```

So you can turn a dictionary into a list of pairs, process the list, and turn it back.

## Two loop variables in action

Here is a loop that finds the most expensive item, now with unpacking.

```python
best_item = None
best_price = None
for item, price in prices.items():
    if best_price is None or price > best_price:
        best_item = item
        best_price = price
print(best_item, best_price)    # rice 5
```

It starts with `None` to mean "nothing seen yet". The first pair always wins, and after that only a higher price replaces it.

## Looping with two nested ideas

You can also unpack inside a loop over a list of tuples.

```python
visits = [("mon", "home"), ("mon", "shop"), ("tue", "home")]
for day, page in visits:
    print(day, page)
```

The list holds tuples, so unpacking works exactly as with `.items()`.

## Tuples as dictionary keys

A dictionary key must be something that cannot change. A list cannot be a key, but a tuple can. That is handy when a fact is identified by *two or more* things at once.

Suppose we count visits per day *and* page:

```python
visits = [("mon", "home"), ("mon", "shop"), ("mon", "home")]
counts = {}
for visit in visits:
    counts[visit] = counts.get(visit, 0) + 1
print(counts)
# {('mon', 'home'): 2, ('mon', 'shop'): 1}
```

Each key is a whole tuple. To look one up, use a tuple too.

```python
print(counts[("mon", "home")])     # 2
print(counts[("tue", "home")])     # KeyError
```

The same trick stores a grid. The key is `(row, column)`:

```python
grid = {}
grid[(0, 0)] = "X"
grid[(0, 1)] = "O"
print(grid.get((1, 1), "."))       # .
```

Writing `grid[0, 1]` without extra brackets also works, because the comma makes the tuple.

## Debugging shape errors

When a loop like `for a, b in something` fails, Python tells you what it found: "too many values to unpack" or "cannot unpack non-iterable int object". Both mean the items are not the shape you thought. Print one item and its type before the loop:

```python
for thing in something:
    print(thing, type(thing))
    break
```

Looping over a plain dictionary gives keys (strings), which is why `for k, v in d:` fails and `for k, v in d.items():` works.

## Common mistakes

- Writing `for k, v in d` instead of `d.items()`.
- Using a list as a key: `d[[1, 2]]` raises `TypeError: unhashable type`.
- Looking up a pair in the wrong order: `("home", "mon")` is a different key from `("mon", "home")`.
- Forgetting the first-time case for a counter, which needs `.get(key, 0)`.
