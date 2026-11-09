+++
id = "foundations.values-and-types"
title = "Values, variables and types"
minutes = 25
+++

# Values, variables and types

In SQL every column has a type and the engine enforces it. Python has types too, but they attach to **values**, not to names, and nothing stops you from putting a string where a number should be, until the program crashes. Learning to *see* types is the single most useful habit in this stage.

> **SQL bridge.** `CAST('42' AS INT)` → `int("42")`. `'a' || 'b'` → `"a" + "b"`. `NULL` → `None`. `TRUE/FALSE` → `True/False`.

## The five types you'll use constantly

```python
print(type(42))        # int    ~ INTEGER
print(type(3.14))      # float  ~ FLOAT/DOUBLE
print(type("hello"))   # str    ~ VARCHAR
print(type(True))      # bool   ~ BOOLEAN
print(type(None))      # NoneType ~ NULL
```

Press **Run** on any example in a lesson. Change it and run it again. Breaking things on purpose is how you learn what the error messages mean.

## Variables are labels

`=` doesn't compare, it *attaches a name to a value*.

```python
price = 19.99
qty = 3
total = price * qty
print(total)
```

You can re-attach a name at any time, even to a different type:

```python
x = 10
x = "ten"
print(x, type(x))
```

That flexibility is why Python programs get type bugs that a warehouse would reject at insert time. Later (Stage 3) you'll add *type hints* and a checker to get that safety back.

## Conversions are explicit

Data from files and APIs arrives as **text**. Everything in a CSV is a `str` until *you* convert it.

```python
raw = "42"
print(raw + raw)          # text joined
print(int(raw) + int(raw))  # numbers added
```

This fails, so read the error. The last line of a traceback is the part that matters:

```python
print("Total: " + 42)
```

## Numbers

```python
print(7 / 2)    # 3.5  true division, always a float
print(7 // 2)   # 3    floor division
print(7 % 2)    # 1    remainder (like MOD)
print(2 ** 10)  # 1024 power
print(round(2.675, 2))
```

Floats are binary approximations. Never trust them for money:

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

For currency use integer cents, or `decimal.Decimal` (covered in the data-wrangling stage).

## Strings

```python
name = "  Ada Lovelace "
print(name.strip())              # TRIM
print(name.strip().upper())      # UPPER
print(name.strip().split(" "))   # SPLIT -> a list
print("lovelace" in name.lower())  # LIKE '%lovelace%'
print(name.strip()[0:3])         # SUBSTR (0-based, end exclusive)
```

Strings are **immutable**: methods return a *new* string. `name.strip()` alone does nothing to `name`.

### f-strings: how you'll build most text

```python
who, n, price = "Ada", 3, 4.5
print(f"{who} bought {n} items at ${price:.2f} = ${n * price:,.2f}")
```

Anything inside `{}` is real Python. After the colon is a format spec: `.2f` is two decimals, `,` adds thousands separators, `>10` right-aligns to width 10.

## Truthiness and None

```python
for v in [0, 1, "", "a", [], [0], None]:
    print(repr(v), "->", bool(v))
```

Empty things are falsy. `None` means *no value* and must be tested with `is`:

```python
result = None
print(result is None)
print(result == None)   # works, but is not idiomatic
```

## What to take away

1. Types belong to values; use `type()` and `repr()` to look.
2. Text from outside needs explicit conversion.
3. Strings are immutable; methods return new strings.
4. f-strings for building text.
5. `None` ≈ `NULL`; test it with `is None`.
