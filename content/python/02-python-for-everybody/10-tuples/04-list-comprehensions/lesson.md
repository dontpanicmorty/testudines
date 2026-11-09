+++
id = "everybody.tuples.list-comprehensions"
title = "List comprehensions and shapes of data"
minutes = 25
+++

# List comprehensions and shapes of data

You have written many loops that build a new list: start with an empty list, loop, maybe test something, append. Python has a compact way to write this pattern, called a **list comprehension**.

## From loop to comprehension

Here is a loop that squares each number.

```python
nums = [1, 2, 3, 4]
squares = []
for n in nums:
    squares.append(n * n)
print(squares)    # [1, 4, 9, 16]
```

The same thing as a comprehension:

```python
squares = [n * n for n in nums]
```

Read it left to right: "make a list of `n * n` for each `n` in `nums`." The square brackets say a list is being built. The part before `for` is what goes into the list. The part after is an ordinary loop header.

## Adding a filter

Put an `if` at the end to keep only some items.

```python
evens = [n for n in nums if n % 2 == 0]
print(evens)      # [2, 4]
```

Equivalent loop:

```python
evens = []
for n in nums:
    if n % 2 == 0:
        evens.append(n)
```

You can combine a calculation and a filter:

```python
big_squares = [n * n for n in nums if n > 2]    # [9, 16]
```

## With strings and tuples

Comprehensions work on anything you can loop over.

```python
names = ["  maya ", "TOMAS", "priya  "]
tidy = [name.strip().title() for name in names]
print(tidy)       # ['Maya', 'Tomas', 'Priya']
```

You can unpack pairs in the loop header, just like in a `for` loop.

```python
prices = {"tea": 3, "milk": 2}
labels = [f"{item}: {cost}" for item, cost in prices.items()]
print(labels)     # ['tea: 3', 'milk: 2']
```

A tuple version of "decorate" is one line:

```python
flipped = [(cost, item) for item, cost in prices.items()]
```

And `sorted()` happily accepts a comprehension:

```python
cheap_first = sorted([(cost, item) for item, cost in prices.items()])
```

## Rows and columns

A list of lists can hold a table.

```python
table = [[1, 2, 3],
         [4, 5, 6]]
```

`table[1][2]` is `6`: second row, third column. A comprehension can pull out a column:

```python
second_column = [row[1] for row in table]
print(second_column)     # [2, 5]
```

## When not to use one

If a comprehension needs more than one short idea, a regular loop is easier to read. Clever is not the goal; clear is. Also, a comprehension builds a whole list in memory, so do not use it just to run something like `print` on each item.

## Debugging "shape" errors

Almost every error in this chapter is about the **shape** of data: how many items, and how they are nested. Habits that help:

- Print `type(x)` and `len(x)` before unpacking or indexing.
- Print one item (`print(data[0])`) to see its real structure.
- Start with a tiny list of two or three items.
- Compare the shape you expect with the shape you have: `[(1, 2), (3, 4)]` is a list of pairs; `[1, 2, 3, 4]` is a flat list.

Typical messages and meanings:

- `IndexError: list index out of range`: a row is shorter than you assumed.
- `ValueError: too many values to unpack`: a tuple has more items than names.
- `TypeError: 'int' object is not iterable`: you are looping over a single number, not a collection.

## Common mistakes

- Forgetting the square brackets and ending up with something that is not a list.
- Putting the `if` before the `for`: `[n if n > 2 for n in nums]` is an error. The filter goes at the end.
- Writing a long, nested comprehension nobody can read.
- Using a comprehension when you really need the result changed in place.
