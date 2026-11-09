+++
id = "foundations.functions"
title = "Functions"
minutes = 30
+++

# Functions

A function is a named, reusable transformation, the Python cousin of a dbt macro or a SQL UDF. Production Python is mostly small functions that take values in and hand a value back. Get comfortable with them now.

> **SQL bridge.** A scalar UDF: `CREATE FUNCTION clean(x) …` → `def clean(x): …`. A dbt macro with arguments and defaults is the closest daily-life analogue.

## def and return

```python
def total(price, qty):
    return price * qty

print(total(4.5, 3))
```

`def` defines, the indented body runs only when called, and `return` hands a value back and **ends the function**.

## return versus print

The most common beginner confusion. `print` shows text to a human; `return` gives a value to the caller.

```python
def show_total(price, qty):
    print(price * qty)      # shows it, returns None

def calc_total(price, qty):
    return price * qty      # gives it back

a = show_total(2, 3)
b = calc_total(2, 3)
print("a is", a)
print("b is", b)
```

> **Predict first.** What is `a`? A function with no `return` returns `None`, so `a is None`. Library functions almost always `return`; printing belongs at the edges of your program.

## Arguments: positional, keyword, defaults

```python
def fmt_name(first, last, upper=False):
    name = f"{last}, {first}"
    return name.upper() if upper else name

print(fmt_name("Ada", "Lovelace"))
print(fmt_name("Ada", "Lovelace", upper=True))
print(fmt_name(last="Hopper", first="Grace"))
```

Keyword arguments make calls self-documenting (`upper=True` beats a bare `True`). Parameters with defaults must come after those without.

## *args and **kwargs

`*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict.

```python
def describe(*args, **kwargs):
    print(args, kwargs)

describe(1, 2, source="csv", limit=10)

def total_all(*amounts):
    return sum(amounts)

print(total_all(1, 2, 3))

nums = [4, 5, 6]
print(total_all(*nums))   # * unpacks a list into arguments
```

Wrapper functions use `**kwargs` to pass options through to another function.

## The mutable default trap

> **Predict first.** What does this print?

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("a"))
print(add_tag("b"))
```

It prints `['a']` then `['a', 'b']`. The default list is created **once**, when `def` runs, and shared by every call. The fix is the `None` sentinel:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag("a"))
print(add_tag("b"))
```

Never use `[]`, `{}` or `set()` as a default value.

## Scope

Names assigned inside a function are **local**; they vanish when it returns. Reading an outer name works; assigning creates a new local.

```python
rate = 0.2

def with_tax(x):
    rate = 0.5          # a new local, the outer rate is untouched
    return x * (1 + rate)

print(with_tax(100), rate)
```

Avoid `global`. If a function needs a value, pass it in; if it produces one, return it. Functions that depend only on their inputs are easy to test and reason about.

## Docstrings and small pure functions

```python
def normalise_email(email):
    """Return the email trimmed and lowercased, or None if blank."""
    cleaned = email.strip().lower()
    return cleaned or None

print(normalise_email("  Ada@Example.COM "))
print(normalise_email("   "))
print(normalise_email.__doc__)
```

A **pure** function has no side effects: same inputs, same output, nothing modified elsewhere. Aim for functions that do one thing, fit on a screen and are named for what they return (`normalise_email`, not `process`).

Pipelines compose them:

```python
def parse_amount(text):
    return float(text.strip().replace("$", "").replace(",", ""))

def with_vat(amount, rate=0.2):
    return round(amount * (1 + rate), 2)

print(with_vat(parse_amount(" $1,000.00 ")))
```

## Common mistakes

```python
# no-run
def greet(name):
    return "hi " + name
greet()
```

```text
TypeError: greet() missing 1 required positional argument: 'name'
```

Too many arguments gives `TypeError: greet() takes 1 positional argument but 2 were given`. Forgetting the parentheses (`greet` instead of `greet(...)`) gives you the function object, not its result. Using a variable before assigning in the function gives `UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`.

Also: returning inside a loop on the first pass when you meant to return after it.

## What to take away

1. `return` gives a value to the caller; `print` only shows it. No `return` means `None`.
2. Use keyword arguments and defaults; `*args`/`**kwargs` collect extras.
3. Never use a mutable default; use `None` and create inside.
4. Variables assigned in a function are local; pass values in, return values out.
5. Write small pure functions with a one-line docstring.
