+++
id = "classes-dataclasses-typing.classes-from-first-principles"
title = "Classes from first principles"
minutes = 30
+++

# Classes from first principles

So far your data has been dicts and lists, and your behaviour has been functions. A **class** bundles the two: a thing that remembers some **state** and knows some **behaviour** that works on it. You already use classes constantly (`str`, `list`, `datetime`, a database connection). Now you write your own.

> **SQL bridge.** A class is a table plus the stored procedures that maintain it, with one important difference: each *instance* is one row that carries its own copy of the columns and the verbs that act on it. `conn.execute(sql)` reads as "this connection, run this".

## Dict plus functions: the version you know

Track how a load went:

```python
def new_stats():
    return {"rows_read": 0, "rows_rejected": 0}

def record(stats, ok):
    stats["rows_read"] += 1
    if not ok:
        stats["rows_rejected"] += 1

s = new_stats()
for ok in [True, True, False]:
    record(s, ok)
print(s)
```

It works, but nothing ties `record` to `s`; a typo like `stats["rows_rejcted"]` creates a new key silently. A class closes these gaps.

## The same thing as a class

```python
class RunStats:
    def __init__(self):
        self.rows_read = 0
        self.rows_rejected = 0

    def record(self, ok):
        self.rows_read += 1
        if not ok:
            self.rows_rejected += 1

s = RunStats()
for ok in [True, True, False]:
    s.record(ok)
print(s.rows_read, s.rows_rejected)
```

Read it piece by piece:

- `class RunStats:` defines a new type. Calling `RunStats()` creates an **instance** (one object).
- `__init__` is the **initializer**; it runs automatically on creation and sets up the starting state.
- `self` is the instance the method is working on. `s.record(ok)` is sugar for `RunStats.record(s, ok)`; Python passes `s` as `self` for you.
- `self.rows_read` is an **attribute**: state stored on *this* instance.

Two instances don't share state:

```python
class RunStats:
    def __init__(self):
        self.rows_read = 0
        self.rows_rejected = 0

    def record(self, ok):
        self.rows_read += 1
        if not ok:
            self.rows_rejected += 1

a, b = RunStats(), RunStats()
a.record(False)
print(a.rows_rejected, b.rows_rejected)
```

## Derived values: methods and properties

Anything computed from state belongs as a method, or as a property if it reads like data:

```python
class RunStats:
    def __init__(self):
        self.rows_read = 0
        self.rows_rejected = 0

    def record(self, ok):
        self.rows_read += 1
        self.rows_rejected += 0 if ok else 1

    @property
    def reject_rate(self):
        return self.rows_rejected / self.rows_read if self.rows_read else 0.0

s = RunStats()
for ok in [True, False, True, True]:
    s.record(ok)
print(s.reject_rate)
```

`@property` lets callers write `s.reject_rate` (no parentheses) while the value is computed fresh every time.

## `__repr__`: make objects printable

Without it, printing an instance gives something unhelpful:

```python
class Plain:
    def __init__(self):
        self.x = 1

print(Plain())
```

The output shows a memory address, useless in logs. Define `__repr__` to return the string you'd want to see while debugging:

```python
class Watermark:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f"Watermark({self.value!r})"

print(Watermark("2025-01-05"))
print([Watermark(), Watermark("x")])
```

Convention: make it look like the constructor call. Special methods like `__init__` and `__repr__` (the "dunder" methods, for double underscore) are hooks Python calls for you.

## A trap: class attributes are shared

An attribute assigned in the class body (outside `__init__`) belongs to the **class**, so all instances see it:

> **Predict first.** Two `Job` objects; one adds an error. How many errors does the *other* one have?

```python
class Job:
    errors = []                 # one list, shared by every Job

    def fail(self, msg):
        self.errors.append(msg)

a, b = Job(), Job()
a.fail("boom")
print(b.errors)
```

One. The fix is to create the list per instance, in `__init__`: `self.errors = []`. This is the most common first bug with classes (and it is the same reason you must never use `[]` as a default argument).

## When NOT to use a class

Many beginners from a SQL/script background over-class. Ask first:

- **No state to remember?** Use a function (or several in a module). A class with only `__init__` and one method is a function wearing a costume.
- **Just a bundle of fields?** Use a `dataclass` (next lesson) or a dict. You don't need hand-written methods.
- **Only grouping related functions?** A module is already a namespace.
- **State plus behaviour that must stay consistent** (a connection, a cursor, a stats counter, a watermark that may only move forward)? That is the sweet spot for a class.

## Common mistakes

- Forgetting `self`: `TypeError: RunStats.record() takes 1 positional argument but 2 were given`. Every method needs `self` first.
- Assigning without `self.`: `rows_read = 0` inside `__init__` makes a throwaway local variable, then `AttributeError: 'RunStats' object has no attribute 'rows_read'`.
- Mutable class attributes (shown above).
- Calling the class without parentheses (`s = RunStats`) and wondering why methods say `missing 1 required positional argument: 'self'`.

## What to take away

1. A class bundles state (attributes) with behaviour (methods); an instance is one object of that type.
2. `__init__` sets up per-instance state; `self` is the instance.
3. Compute derived values with methods or `@property`.
4. Define `__repr__` so logs and debuggers show something useful.
5. State created in the class body is shared; create per-instance state in `__init__`.
6. If there's no state to protect, a plain function is better than a class.
