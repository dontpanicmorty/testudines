+++
id = "errors-and-logging.defensive-code"
title = "Defensive code and validation"
minutes = 30
+++

# Defensive code and validation

A warehouse protects you with constraints: `NOT NULL`, typed columns, `UNIQUE` (if enforced), dbt `not_null` and `accepted_values` tests. Python data has no such shield. Anything that crosses into your program from a file, API or user is **untrusted** until you check it. Production code puts that checking in one place, at the boundary, and keeps everything inside clean.

> **SQL bridge.** A dbt staging model casts and cleans; downstream models trust it. Validation at the boundary is your Python staging layer.

## Validate at the boundary

Write a function that takes a raw dict and either returns a clean, typed record or raises a clear error. Everything after it can assume good data.

```python
class ValidationError(ValueError):
    pass

def validate_order(raw):
    errors = []
    order_id = (raw.get("order_id") or "").strip()
    if not order_id:
        errors.append("order_id is required")
    try:
        qty = int(raw.get("quantity", ""))
        if qty <= 0:
            errors.append("quantity must be positive")
    except ValueError:
        errors.append(f"quantity is not an integer: {raw.get('quantity')!r}")
        qty = None
    if errors:
        raise ValidationError("; ".join(errors))
    return {"order_id": order_id, "quantity": qty}

print(validate_order({"order_id": " A1 ", "quantity": "3"}))
try:
    validate_order({"order_id": "", "quantity": "x"})
except ValidationError as e:
    print("invalid:", e)
```

Collect **all** the problems in a row rather than stopping at the first; whoever fixes the data will thank you.

## Fail loudly or quarantine?

Two honest strategies for a bad row, and the choice is a business decision:

- **Fail loudly.** Stop the run. Right when bad data means something upstream is broken (the whole file has the wrong columns) or correctness matters more than freshness (financial totals).
- **Quarantine.** Set the bad rows aside with a reason, process the rest, and report counts. Right for row-level noise in large feeds.

Never choose the third option: silently dropping or "fixing" rows with no record.

```python
class ValidationError(ValueError):
    pass

def validate_order(raw):
    if not raw["order_id"] or int(raw["quantity"]) <= 0:
        raise ValidationError("order_id required and quantity must be positive")
    return raw

def split_valid(rows, validate):
    good, rejected = [], []
    for n, raw in enumerate(rows, start=1):
        try:
            good.append(validate(raw))
        except ValidationError as e:
            rejected.append({"row": n, "reason": str(e), "raw": raw})
    return good, rejected

rows = [
    {"order_id": "A1", "quantity": "2"},
    {"order_id": "A2", "quantity": "0"},
    {"order_id": "", "quantity": "5"},
]
good, rejected = split_valid(rows, validate_order)
print(len(good), "good")
for r in rejected:
    print(r["row"], r["reason"])
```

A reasonable hybrid: quarantine, but **fail the run if the rejected share exceeds a threshold** (say 5%), because a sudden spike usually means a broken source, not noisy rows.

```python
def check_reject_rate(total, rejected, max_rate=0.05):
    rate = rejected / total if total else 0
    if rate > max_rate:
        raise RuntimeError(f"{rejected}/{total} rows rejected ({rate:.0%}), limit {max_rate:.0%}")

check_reject_rate(100, 3)
try:
    check_reject_rate(100, 40)
except RuntimeError as e:
    print(e)
```

## Guard clauses

Handle bad cases first and return or raise early. The happy path stays flat and readable.

```python
def net_amount(row):
    if row is None:
        raise ValueError("row is required")
    if row["status"] == "void":
        return 0
    if row["amount"] is None:
        raise ValueError("amount missing")
    return row["amount"] - row.get("discount", 0)

print(net_amount({"status": "paid", "amount": 100, "discount": 15}))
print(net_amount({"status": "void", "amount": 100}))
```

Compare with the nested `if ... else` pyramid that does the same: three more levels of indentation and no more safety.

## Assertions are not validation

`assert` states something that **must** be true if the program is correct, a bug-catcher for you, the developer.

```python
def mean(values):
    assert values, "mean() called with no values; caller bug"
    return sum(values) / len(values)

print(mean([1, 2, 3]))
```

Two reasons it must not validate input. Running Python with `-O` strips every `assert` out. And a failed assert raises `AssertionError`, which no caller should be expected to handle. Rule of thumb:

| Situation | Tool |
|---|---|
| Data from outside might be bad | `if ... raise ValueError / custom error` |
| "This can never happen unless I wrote a bug" | `assert` |
| Tests | `assert` (pytest rewrites them to show values) |

## Don't mutate your inputs, and prefer explicit defaults

Defensive code also avoids hidden state. The classic trap:

> **Predict first.** What does the second call print?

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("a"))
print(add_tag("b"))
```

The default list is created **once**, at definition time, and shared across calls. Use `None` as the sentinel:

```python
def add_tag(tag, tags=None):
    tags = [] if tags is None else list(tags)
    tags.append(tag)
    return tags

print(add_tag("a"))
print(add_tag("b"))
```

## Common mistakes

- Validating deep inside the pipeline, so some code paths see unclean data.
- `int(x) if x else 0` which turns a missing value into a plausible-looking zero. Decide whether missing means zero or unknown.
- Catching the validation error and discarding the reason.
- Using `assert` to check user input, then wondering why prod accepts it under `python -O`.

## What to take away

1. Validate once at the boundary; return clean typed records or raise.
2. Report every problem in a row, not just the first.
3. Fail loudly or quarantine with reasons; never silently drop.
4. Guard clauses keep the happy path flat.
5. `assert` is for bugs, `raise` is for bad data.
6. Never use a mutable default argument.
