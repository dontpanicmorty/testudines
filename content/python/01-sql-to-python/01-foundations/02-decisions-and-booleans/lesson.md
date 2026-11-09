+++
id = "foundations.decisions-and-booleans"
title = "Decisions and booleans"
minutes = 25
+++

# Decisions and booleans

Every `CASE WHEN` and every `WHERE` clause you have written is a decision. Python makes the same decisions with `if`, comparison operators and boolean logic, with one big difference: the structure is shown by **indentation**, not by keywords like `END`.

> **SQL bridge.** `CASE WHEN … THEN … ELSE … END` → `if / elif / else`. `AND / OR / NOT` → `and / or / not`. `x IN (…)` → `x in (…)`. `IS NULL` → `is None`.

## if / elif / else

```python
amount = 120

if amount >= 100:
    tier = "large"
elif amount >= 20:
    tier = "medium"
else:
    tier = "small"

print(tier)
```

Rules: a colon ends the condition line, the body is indented (4 spaces), and branches are tried **top to bottom**; the first true one wins, just like `CASE`. Order your branches from most specific to least specific.

> **Predict first.** If the first two branches were swapped (`>= 20` first), what would `tier` be for `amount = 120`?

```python
amount = 120
if amount >= 20:
    tier = "medium"
elif amount >= 100:
    tier = "large"
else:
    tier = "small"
print(tier)
```

`medium`: the first matching branch wins, so the `large` branch is unreachable. The same bug exists in SQL `CASE`.

## Comparison operators

```python
print(5 == 5)      # equal (two equals signs; one is assignment)
print(5 != 6)      # not equal (SQL <>)
print(3 < 5 <= 5)  # chained: 3 < 5 and 5 <= 5
print("apple" < "banana")  # strings compare alphabetically
```

Chained comparisons are a gift: `18 <= age < 65` replaces `age >= 18 AND age < 65` (and `BETWEEN`, but note `BETWEEN` is inclusive on both ends).

## and, or, not

```python
plan, region, spend = "pro", "EU", 900

print(plan == "pro" and region == "EU")
print(plan == "free" or spend > 500)
print(not (plan == "free"))
```

Precedence is `not`, then `and`, then `or`. When mixing `and` with `or`, add parentheses; your reader (and future you) should not have to remember the table. Python also **short-circuits**: in `a and b`, if `a` is false `b` is never evaluated. That makes this safe:

```python
row = {}
print("email" in row and row["email"].endswith(".com"))
```

## Membership with `in`

```python
status = "shipped"
print(status in ("shipped", "delivered"))      # IN (...)
print(status not in ("cancelled", "returned")) # NOT IN (...)
print("ship" in status)                        # substring, like LIKE '%ship%'
```

Use a tuple or set for the options. Note one difference from SQL: Python has no three-valued logic. `x in (...)` is always `True` or `False`, never "unknown".

## None checks: your IS NULL

```python
discount = None

if discount is None:
    print("no discount recorded")

# Beware: 0 is a real value, but it is falsy
discount = 0
if not discount:
    print("treated as missing (wrong!)")
if discount is None:
    print("never printed")
```

`if not x` conflates `None`, `0`, `""` and `[]`. When a missing value and a zero mean different things (they usually do in data work), test `is None` explicitly.

## The conditional expression (ternary)

The `CASE` that fits on one line:

```python
qty = 0
label = "in stock" if qty > 0 else "sold out"
print(label)
```

Use it for simple two-way choices. For three or more branches, a normal `if/elif` reads better.

## Early return beats deep nesting

Naive:

```python
def classify(row):
    if row is not None:
        if row.get("amount") is not None:
            if row["amount"] > 0:
                return "paid"
            else:
                return "zero"
        else:
            return "unknown"
    else:
        return "unknown"
```

Idiomatic: handle the odd cases first and exit.

```python
def classify(row):
    if row is None or row.get("amount") is None:
        return "unknown"
    if row["amount"] > 0:
        return "paid"
    return "zero"

print(classify({"amount": 5}), classify({}), classify(None), classify({"amount": 0}))
```

Flat code is easier to test: each `return` is one case.

## Common mistakes

```python
# no-run
x = 5
if x = 5:
    print("five")
```

```text
SyntaxError: invalid syntax. Maybe you meant '==' instead of '='?
```

Use `==` to compare. Another classic:

```python
status = "paid"
print(status == "paid" or "refunded")   # always truthy!
```

`status == "refunded"` is never evaluated by the right-hand string; `"refunded"` on its own is truthy. Write `status in ("paid", "refunded")`.

Last one: `if x == None` works but `is None` is the idiom, and `if x == True` should just be `if x`.

## What to take away

1. `if/elif/else` is `CASE`; the first true branch wins, so order matters.
2. `and/or/not`, with parentheses whenever you mix them; chained comparisons like `a <= x < b`.
3. `in` replaces `IN`, and works on strings as substring tests.
4. Use `is None` for missing values; `not x` also catches `0` and `""`.
5. Return early to keep functions flat.
