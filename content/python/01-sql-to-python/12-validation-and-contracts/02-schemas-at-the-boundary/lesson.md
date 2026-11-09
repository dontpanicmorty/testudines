+++
id = "validation-and-contracts.schemas-at-the-boundary"
title = "Schemas at the boundary"
minutes = 30
+++

# Schemas at the boundary

Last lesson, one bad row raised an exception. In a pipeline that is rarely what you want: 1 corrupt row out of a million should not kill the load, and it should not slip into the warehouse either. The production answer is the same one you use in a warehouse: **quarantine**. Good rows continue; bad rows go to a reject table with the reason.

> **SQL bridge.** Think `INSERT ... SELECT` with a `WHERE` for valid rows, and a second statement writing the rejected rows plus a reason column into `rejects`. dbt's `store_failures` for tests does the same.

## Catch per row, not per batch

```python
from pydantic import BaseModel, ValidationError

class Order(BaseModel):
    order_id: int
    amount: float

rows = [{"order_id": "1", "amount": "9.5"}, {"order_id": "x", "amount": "3"}, {"order_id": "3", "amount": "7"}]

good, bad = [], []
for i, row in enumerate(rows):
    try:
        good.append(Order.model_validate(row))
    except ValidationError as exc:
        bad.append({"index": i, "row": row, "errors": exc.errors()})

print(len(good), "good,", len(bad), "bad")
print(bad[0]["errors"][0]["loc"], bad[0]["errors"][0]["msg"])
```

The `try` goes *inside* the loop and only around the validation. Wrapping the whole loop would stop at the first failure.

## Make the errors portable

`exc.errors()` contains objects (like the original exception and input) that are awkward to write to a file. Reduce each error to plain, stable values:

```python
from pydantic import BaseModel, ValidationError

class Order(BaseModel):
    order_id: int
    amount: float

def simple_errors(exc: ValidationError) -> list[dict]:
    return [
        {"field": ".".join(str(p) for p in e["loc"]) or "__row__", "message": e["msg"], "code": e["type"]}
        for e in exc.errors()
    ]

try:
    Order.model_validate({"order_id": "x"})
except ValidationError as exc:
    for item in simple_errors(exc):
        print(item)
```

Two errors came from one row: `order_id` is not an integer, and `amount` is missing. Keep them all; a reject row should say everything that is wrong, so a human can fix the source in one pass.

## A reusable partition function

Wrap the pattern once, with the model as a parameter:

```python
from pydantic import BaseModel, ValidationError

def partition(rows, model: type[BaseModel]):
    valid, rejects = [], []
    for index, row in enumerate(rows):
        try:
            valid.append(model.model_validate(row))
        except ValidationError as exc:
            rejects.append({
                "index": index,
                "row": row,
                "errors": [{"field": ".".join(map(str, e["loc"])), "message": e["msg"]} for e in exc.errors()],
            })
    return valid, rejects

class Event(BaseModel):
    event_id: str
    user_id: int

valid, rejects = partition([{"event_id": "a", "user_id": 1}, {"event_id": "b"}], Event)
print(len(valid), rejects)
```

`index` is the position in the source so the bad record can be found again. Keep the original row too: never throw away data you could not parse.

## Bad JSON is also a boundary problem

The bundled `events.jsonl` has three corrupt lines. A line can fail in two different ways: it is not JSON at all, or it is JSON with the wrong shape. Treat both as rejects:

```python
import json

lines = ['{"event_id": "a", "user_id": 1}', '{"event_id": "b", "user_', '[1, 2, 3]']
parsed, rejects = [], []
for i, line in enumerate(lines):
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as exc:
        rejects.append({"index": i, "reason": f"invalid json: {exc.msg}"})
        continue
    if not isinstance(obj, dict):
        rejects.append({"index": i, "reason": "not an object"})
        continue
    parsed.append(obj)
print(len(parsed), rejects)
```

## Error reports

A pile of rejects is useless unless someone reads it. Summarise by field so the *pattern* is visible:

```python
from collections import Counter

rejects = [
    {"index": 1, "errors": [{"field": "amount", "message": "bad"}]},
    {"index": 4, "errors": [{"field": "amount", "message": "bad"}, {"field": "status", "message": "bad"}]},
    {"index": 9, "errors": [{"field": "status", "message": "bad"}]},
]
by_field = Counter(e["field"] for r in rejects for e in r["errors"])
print(by_field.most_common())
```

"40 failures, all on `amount`" tells you the upstream format changed. "40 failures, all different" tells you the data is just dirty. That distinction is worth gold when you triage.

## A circuit breaker

Quarantine protects against stray bad rows. It must not hide a catastrophe: if 90% of rows fail, the schema changed and loading the remaining 10% would be misleading. Fail the run when the reject rate crosses a threshold:

```python
def check_reject_rate(n_valid: int, n_rejected: int, max_rate: float = 0.05) -> None:
    total = n_valid + n_rejected
    if total and n_rejected / total > max_rate:
        raise RuntimeError(f"{n_rejected}/{total} rows rejected, over the {max_rate:.0%} limit")

check_reject_rate(98, 2)
print("ok")
try:
    check_reject_rate(10, 90)
except RuntimeError as exc:
    print("stopped:", exc)
```

## Common mistakes

- Putting the `try` around the whole loop: the first bad row aborts everything and the rest is never read.
- Catching `Exception` broadly: you swallow real bugs (a typo in your code) as "bad data". Catch `ValidationError` and `json.JSONDecodeError` specifically.
- Storing only the error message and not the raw row: you cannot reprocess after the fix.
- Quarantining silently: log the counts and make the run fail past a threshold.
- `TypeError: Object of type ValidationError is not JSON serializable` when writing `exc.errors()` straight to JSON; convert to plain dicts first.

## What to take away

1. Validate per row, catch `ValidationError` inside the loop, and keep going.
2. A reject keeps the index, the raw row and every error, as plain serialisable values.
3. Parse failures (bad JSON) and shape failures (bad fields) both go to rejects.
4. Summarise rejects by field to see whether it is a format change or just dirty data.
5. Add a reject-rate limit so quarantine cannot hide a broken source.
