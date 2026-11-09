+++
id = "everybody.tuples.tuples-and-assignment"
title = "Tuples and tuple assignment"
minutes = 25
+++

# Tuples and tuple assignment

A **tuple** (say "too-pull" or "tup-ul") is a lot like a list: an ordered group of values you reach by position. There is one big difference. A tuple can **never be changed** once it is made. The fancy word for this is **immutable**. A list, which can be changed, is **mutable**.

## Making tuples

Tuples are usually written with round brackets.

```python
point = (3, 7)
colors = ("red", "green", "blue")
print(point[0])        # 3
print(colors[1:])      # ('green', 'blue')
print(len(colors))     # 3
```

Indexing, slicing, `len()`, `in` and looping all work just as they do for lists. A tuple with one item needs a trailing comma, otherwise the brackets are just maths brackets.

```python
one = (5,)       # a tuple with one value
not_one = (5)    # just the number 5
```

The brackets are actually optional: `point = 3, 7` makes the same tuple. We use brackets because they are easier to read.

## What "immutable" means

Try to change a tuple and Python refuses.

```python
point = (3, 7)
point[0] = 10     # TypeError: 'tuple' object does not support item assignment
```

You also cannot `append`, `sort` or `remove`. If you need a different tuple, build a new one.

```python
point = (10,) + point[1:]
print(point)      # (10, 7)
```

Why would anyone want something that cannot change? Because it is safe: nothing can alter it behind your back. And because it never changes, a tuple can be used as a dictionary key, which you will see in the next lesson. Use tuples for small, fixed groups of related facts, such as `(latitude, longitude)` or `(year, month, day)`.

## Comparing tuples

Tuples compare **one position at a time, from the left**. Python looks at the first items. If they differ, that decides the answer. Only if they are equal does it look at the second items, and so on.

```python
print((1, 9) < (2, 0))      # True: 1 is less than 2
print((1, 9) < (1, 10))     # True: first equal, 9 < 10
print(("tea", 3) > ("tea", 2))   # True
```

This is how dictionaries of words are sorted, and you will use it in the sorting lesson.

## Tuple assignment

You can put a tuple on the left of an `=` and fill several names in one go.

```python
point = (3, 7)
x, y = point
print(x, y)     # 3 7
```

The number of names on the left must match the number of values on the right. Otherwise you get a `ValueError`.

```python
a, b, c = point    # ValueError: not enough values to unpack
```

### Swapping two values

This gives Python a tidy way to swap two variables without a helper.

```python
a = "first"
b = "second"
a, b = b, a
print(a, b)     # second first
```

The right side is worked out completely before anything is stored on the left, so no value gets overwritten too soon.

### Splitting text

The right side can be anything that gives the right number of pieces.

```python
name, domain = "maya@example.org".split("@")
print(name)      # maya
print(domain)    # example.org
```

### Returning two things from a function

A function can only return one object, but that object can be a tuple.

```python
def low_high(numbers):
    return min(numbers), max(numbers)

low, high = low_high([4, 9, 2])
print(low, high)    # 2 9
```

## Strings, lists and tuples compared

All three are ordered, can be indexed and sliced, and can be looped over. The differences:

- A **string** holds only characters and is immutable.
- A **list** holds anything and is mutable.
- A **tuple** holds anything and is immutable.

Convert between them with `list(t)` and `tuple(x)`.

## Debugging tip: shape errors

Many tuple bugs are "shape" errors: the data is not the size or nesting you assumed. Print `len(x)` and `type(x)` before unpacking. The message "too many values to unpack" means the right side is longer than your list of names.

## Common mistakes

- Forgetting the comma in a one-item tuple: `(5)` is an integer.
- Trying to modify a tuple with `t[0] = ...` or `t.append(...)`.
- Unpacking into the wrong number of names.
- Expecting `(1, 2) < (1, 2, 0)` to be false. A shorter tuple that matches so far is considered smaller.
