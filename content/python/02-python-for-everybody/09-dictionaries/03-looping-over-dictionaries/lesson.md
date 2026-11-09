+++
id = "everybody.dictionaries.looping-over-dictionaries"
title = "Looping over dictionaries"
minutes = 25
+++

# Looping over dictionaries

Once a dictionary holds your data, you will want to walk through it: print every entry, add up the values, pick out the interesting pairs. This lesson shows the ways to loop and how to put the output in a sensible order.

We will use this small dictionary of stock levels throughout.

```python
stock = {"pears": 4, "apples": 12, "plums": 0, "figs": 7}
```

## A plain `for` loop gives keys

When you loop over a dictionary, you get its **keys**, one at a time.

```python
for name in stock:
    print(name)
```

If you also want the value, look it up with the key.

```python
for name in stock:
    print(name, stock[name])
```

This prints each name beside its stock count. In modern Python the pairs come out in the order they were first added, so you will see `pears`, `apples`, `plums`, `figs`.

## Looping over values only

If you do not care about the keys, loop over `.values()`.

```python
total = 0
for count in stock.values():
    total = total + count
print(total)    # 23
```

## Looping over keys and values together

The `.items()` method gives you each key and value as a pair, and a `for` loop can unpack the pair into two names at once.

```python
for name, count in stock.items():
    print(name, "->", count)
```

Read `for name, count in stock.items()` as "for each name and count in the stock". It is shorter and clearer than looking each key up again.

## Filtering: only the entries you want

Put an `if` inside the loop to pick out some entries. Here we build a list of everything that is running low.

```python
low = []
for name, count in stock.items():
    if count < 5:
        low.append(name)
print(low)    # ['pears', 'plums']
```

To build a smaller **dictionary** instead, assign into a new one.

```python
in_stock = {}
for name, count in stock.items():
    if count > 0:
        in_stock[name] = count
print(in_stock)
```

## Sorting the keys

Dictionaries remember insertion order, but often you want alphabetical order for a tidy report. `sorted()` takes any collection and returns a new, sorted list. Given a dictionary, it sorts the keys.

```python
for name in sorted(stock):
    print(name, stock[name])
```

This prints `apples`, `figs`, `pears`, `plums`. The dictionary itself is unchanged. `sorted(stock, reverse=True)` sorts from Z to A.

Note that you cannot call `.sort()` on a dictionary; that method belongs to lists. Use `sorted()`.

## Finding the biggest value

A "keep the best so far" loop finds the key with the largest value.

```python
best_name = None
best_count = -1
for name, count in stock.items():
    if count > best_count:
        best_name = name
        best_count = count
print(best_name, best_count)    # apples 12
```

`best_count` starts below any real count, so the first entry always wins the first comparison.

## Do not change a dictionary while you loop over it

Adding or removing keys while looping over the same dictionary makes Python complain with a `RuntimeError`. Build a new dictionary (as we did above) or loop over a copy such as `list(stock)`.

## Debugging tip: sanity checks

After filtering, check the size: `len(in_stock) <= len(stock)` must be true. After summing, compare with a total you can work out by hand on a tiny dictionary. A tiny input that you can check by eye catches most mistakes.

## Common mistakes

- Expecting `for x in d` to give values. It gives keys.
- Writing `for name, count in stock` without `.items()`. Python then tries to split each key string into two pieces and fails.
- Calling `d.sort()`. Dictionaries have no `.sort()`; use `sorted(d)`.
- Adding keys to a dictionary during a loop over that same dictionary.
