+++
id = "code-quality.readable-code"
title = "Readable code"
minutes = 30
+++

# Readable code

You have opinions about SQL style already: staging CTEs with clear names, one transformation per CTE, no 400-line `SELECT`. Those habits, applied to Python, are most of what "clean code" means. Code is read many more times than it is written, usually by you in six months with no memory of why.

> **SQL bridge.** A dbt style guide says: name CTEs for what they contain, keep each one focused, and import all sources at the top. In Python: name variables and functions for their meaning, keep each function focused, and keep decisions flat.

## Start with a messy function

Here is a real-looking snippet. It works. Read it and try to say what it does:

```python
def f(d):
    r = []
    for x in d:
        if x["s"] == "paid":
            if x["t"] > 100:
                r.append(x["c"].strip().title() + ": " + str(round(x["t"] * 1.2, 2)))
    return r

orders = [
    {"c": " ada ", "s": "paid", "t": 150},
    {"c": "grace", "s": "open", "t": 500},
    {"c": "linus", "s": "paid", "t": 80},
]
print(f(orders))
```

You can decode it, but you shouldn't have to. We'll refactor in small steps, running the same check after each so we know behaviour didn't change.

## Step 1: names that say what things are

```python
def large_paid_order_lines(orders):
    lines = []
    for order in orders:
        if order["s"] == "paid":
            if order["t"] > 100:
                name = order["c"].strip().title()
                total_with_tax = round(order["t"] * 1.2, 2)
                lines.append(name + ": " + str(total_with_tax))
    return lines

orders = [
    {"c": " ada ", "s": "paid", "t": 150},
    {"c": "grace", "s": "open", "t": 500},
]
print(large_paid_order_lines(orders))
```

Rules: a function is a verb phrase, a variable is a noun that says *what it holds*, avoid single letters (except tiny loop indexes), and don't encode types (`list_of_orders`). Booleans read as questions: `is_paid`, `has_refund`.

## Step 2: replace magic numbers and ugly keys with names

`100` and `1.2` mean something. Give the meaning a name, once:

```python
MIN_LARGE_ORDER = 100
TAX_MULTIPLIER = 1.2

def large_paid_order_lines(orders):
    lines = []
    for order in orders:
        if order["s"] == "paid" and order["t"] > MIN_LARGE_ORDER:
            name = order["c"].strip().title()
            total_with_tax = round(order["t"] * TAX_MULTIPLIER, 2)
            lines.append(f"{name}: {total_with_tax}")
    return lines

orders = [
    {"c": " ada ", "s": "paid", "t": 150},
    {"c": "grace", "s": "open", "t": 500},
]
print(large_paid_order_lines(orders))
```

We also flattened two nested `if`s into one condition and used an f-string instead of `+` and `str()`.

## Step 3: small functions with one job

When a function does filtering, calculating *and* formatting, split it. Each piece becomes testable and nameable:

```python
MIN_LARGE_ORDER = 100
TAX_MULTIPLIER = 1.2

def is_large_paid_order(order):
    return order["s"] == "paid" and order["t"] > MIN_LARGE_ORDER

def format_line(order):
    name = order["c"].strip().title()
    return f"{name}: {round(order['t'] * TAX_MULTIPLIER, 2)}"

def large_paid_order_lines(orders):
    return [format_line(o) for o in orders if is_large_paid_order(o)]

orders = [
    {"c": " ada ", "s": "paid", "t": 150},
    {"c": "grace", "s": "open", "t": 500},
    {"c": "linus", "s": "paid", "t": 80},
]
print(large_paid_order_lines(orders))
```

The top-level function now reads like a sentence: *the formatted lines of the orders that are large and paid*. A good guideline is that a function fits on one screen (about 15-20 lines) and you can name what it does without using the word "and".

## Early returns beat deep nesting

Each nested `if` makes the reader hold one more condition in their head. Handle the unusual cases first and **return early**, leaving the main path unindented:

```python
def shipping_label(order):
    if order is not None:
        if order["status"] == "paid":
            if order["country"] == "US":
                return "domestic"
            else:
                return "international"
        else:
            return "hold"
    else:
        return "missing"

def shipping_label_flat(order):
    if order is None:
        return "missing"
    if order["status"] != "paid":
        return "hold"
    if order["country"] == "US":
        return "domestic"
    return "international"

sample = {"status": "paid", "country": "FR"}
print(shipping_label(sample), shipping_label_flat(sample))
```

Same behaviour, but the second reads top to bottom like a checklist. Aim for at most two levels of indentation inside a function.

## Comments explain why, not what

A comment that restates the code is noise and goes stale. A comment that records a *reason* the code can't show is gold:

```python
# no-run
# bad: says what the code already says
count = count + 1   # add one to count

# good: says why
# The billing export repeats the header row every 10,000 lines; skip them.
rows = [r for r in rows if r[0] != "customer_id"]
```

If you feel you need a comment to explain *what* a block does, extract it into a function with that name instead.

## Other habits worth the effort

- One level of abstraction per function: don't mix parsing characters with business rules.
- Prefer returning values over mutating arguments or globals. It makes behaviour predictable.
- Delete dead code and commented-out code; version control remembers.
- Keep the happy path obvious and the error handling explicit (`raise ValueError("...")` with a message that names the bad value).

## Common mistakes

- "Clever" one-liners with nested comprehensions that nobody can debug. If it needs a comment to decode, write the loop.
- Renaming without running the tests: refactors must preserve behaviour. Refactor in small steps with the tests green.
- Over-abstracting too early: five one-line functions used once each is worse than one clear function. Extract when a name genuinely helps.
- Generic names: `data`, `result`, `temp`, `handle()`, `process()`. Say what it is.
- Mutating a list while looping over it (`for x in items: items.remove(x)`) silently skips elements.

## What to take away

1. Names carry the meaning: verbs for functions, nouns for values, no single letters.
2. Give magic numbers a name and define it once.
3. A function does one job and fits on a screen.
4. Return early to keep the main path flat; avoid more than two nesting levels.
5. Comments explain why. If you're explaining what, extract a function.
6. Refactor in small steps with tests proving behaviour didn't change.
