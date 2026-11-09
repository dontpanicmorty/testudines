+++
id = "everybody.functions.built-in-functions"
title = "Calling functions: built-ins, math and random"
minutes = 25
+++

# Calling functions: built-ins, math and random

You have already used functions: `print`, `input`, `int`, `type`. In this lesson you look at what a function is, and meet some of the most useful ones that come with Python.

## What is a function?

A **function** is a named set of instructions that does a job. You use, or **call**, a function by writing its name followed by brackets. Whatever you put inside the brackets is passed to the function. These values are called **arguments**.

```python
longest = max(4, 19, 7)
print(longest)
```

`max` is the function, and `4, 19, 7` are its arguments. It returns the largest one, `19`, which we store in `longest`. A value a function hands back is called a **return value**.

You do not need to know how a function works inside to use it. You need to know its name, what you give it and what it gives back.

## Built-in functions

Python comes with many functions ready to use. Here are some you will use a lot:

```python
print(max(3, 8, 5))            # 8
print(min(3, 8, 5))            # 3
print(len("banana"))           # 6
print(abs(-12))                # 12
print(round(3.14159, 2))       # 3.14
print(sum([1, 2, 3]))          # 6
```

- `max` and `min` find the largest and smallest. They also work on text, using alphabetical order.
- `len` gives the length of a string: the number of characters.
- `abs` removes a minus sign. `round(number, places)` rounds to a number of decimal places.
- `sum` adds up a collection, such as the list `[1, 2, 3]`. Lists get their own chapter later.

Use them inside expressions like any other value: `max(a, b) - min(a, b)` gives the gap between two numbers.

## Type conversion functions

You met these in chapter 2: `int()`, `float()` and `str()` each take one value and return it converted.

```python
print(int("40") + 2)       # 42
print(float(3))            # 3.0
print(str(99) + " lives")  # 99 lives
print(int(-2.9))           # -2, chops towards zero
```

Conversion fails if the value does not make sense, for example `int("hello")` raises a `ValueError`.

## The math module

Many functions are not built in but are stored in **modules**: files of extra tools. To use a module, **import** it at the top of your program:

```python
import math

print(math.sqrt(49))       # 7.0
print(math.pi)             # 3.141592653589793
print(math.floor(4.8))     # 4
print(math.ceil(4.2))      # 5
print(math.hypot(3, 4))    # 5.0
```

After `import math`, you use a dot to reach things inside the module: `math.sqrt`. The dot says "the `sqrt` that belongs to `math`". `math.pi` is a value, not a function, so it has no brackets.

- `floor` rounds down, `ceil` rounds up.
- `hypot(a, b)` gives the long side of a right-angled triangle with sides a and b.

If you write `sqrt(49)` without the `math.` in front, you get a `NameError`. Python only knows what you import.

## Random numbers

Computers are deterministic, but they can imitate chance with **pseudo-random** numbers: a sequence that looks random but is calculated. The `random` module provides them:

```python
import random

print(random.randint(1, 6))        # a whole number from 1 to 6, both included
print(random.random())             # a float from 0.0 up to (not including) 1.0
print(random.choice(["red", "blue", "green"]))   # one item from the list
```

Each run gives different answers. `randint(1, 6)` includes both 1 and 6, a little like a dice roll.

You can make the sequence repeatable by "seeding" it. After `random.seed(5)`, the same numbers come out each time, which helps when you are testing:

```python
random.seed(5)
first = random.randint(1, 100)
random.seed(5)
second = random.randint(1, 100)
print(first == second)    # True
```

## Common mistakes

- **Forgetting to import.** `math.sqrt(4)` without `import math` is a `NameError`.
- **Forgetting the module name**: writing `sqrt(4)` instead of `math.sqrt(4)`.
- **Naming your own file `random.py` or `math.py`.** Python then imports your file instead of the real module.
- **Forgetting the brackets** when you call a function. `math.sqrt` alone is the function itself, not an answer.
- **Expecting `round` to always round half up.** `round(2.5)` gives `2`; Python rounds to the nearest even number when exactly halfway.
- **Assuming `randint(1, 6)` stops before 6.** It includes it.

## What to take away

1. You call a function with brackets; the values inside are its arguments, and it returns a value.
2. Handy built-ins: `max`, `min`, `len`, `abs`, `round`, `sum`, plus `int`, `float`, `str`.
3. `import math` gives `math.sqrt`, `math.floor`, `math.pi` and more.
4. `import random` gives `random.randint`, `random.random` and `random.choice`.
