+++
id = "validation-and-contracts.pydantic-models"
title = "pydantic models: parse, don't hope"
minutes = 30
+++

# pydantic models: parse, don't hope

A warehouse table rejects a row that violates its column types. Python dictionaries accept anything, so a bad value travels silently until something far downstream breaks. **pydantic** puts a typed gate at the entrance: you declare the shape once, and every row is checked and converted when it enters your program.

> **SQL bridge.** A `BaseModel` is a table definition with constraints (`NOT NULL`, `CHECK`, types). `Model.model_validate(row)` is the `INSERT` that either succeeds or raises. A dbt `accepted_values` or `not_null` test, but at the moment of ingestion.

## A model

```python
from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_id: str
    customer: str
    amount: float
    paid: bool = False          # a default makes the field optional

inv = Invoice(invoice_id="INV-1", customer="Ada", amount=12.5)
print(inv)
print(inv.amount, inv.paid)
print(inv.model_dump())
```

A model is a class where annotations are the schema. Fields without a default are required. `model_dump()` converts back to a plain dict for JSON or a database.

## Coercion: pydantic is helpful by default

Data from CSV files is all text. In the default ("lax") mode pydantic converts what it sensibly can:

```python
from pydantic import BaseModel

class Row(BaseModel):
    qty: int
    price: float
    shipped: bool

print(Row(qty="3", price="9.99", shipped="true"))
```

`"3"` became `3`, `"9.99"` became `9.99`, `"true"` became `True`. Exactly what you want when parsing a CSV row. But coercion has limits: it will not guess nonsense.

```python
from pydantic import BaseModel, ValidationError

class Row(BaseModel):
    qty: int

for bad in [{"qty": "three"}, {"qty": 2.5}, {}]:
    try:
        Row(**bad)
    except ValidationError as exc:
        err = exc.errors()[0]
        print(err["loc"], err["type"], "-", err["msg"])
```

`ValidationError.errors()` is a list of dicts: `loc` (where), `type` (machine-readable code), `msg` (human text). You will build reports from it later.

> **Predict first.** With `qty: int`, does `2.0` pass? What about `2.5`?

`2.0` passes (it is exactly an integer), `2.5` fails because converting it would lose information.

## Strict mode: no conversion

When data should already be typed (it came from JSON or another service), turn coercion off for the model or for a field:

```python
from pydantic import BaseModel, ConfigDict, ValidationError

class StrictRow(BaseModel):
    model_config = ConfigDict(strict=True)
    qty: int

print(StrictRow(qty=3))
try:
    StrictRow(qty="3")
except ValidationError as exc:
    print(exc.errors()[0]["type"])
```

Rule of thumb: **lax at the CSV boundary, strict between your own components.**

## Constraints and `Literal`

```python
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

class Order(BaseModel):
    order_id: int
    status: Literal["placed", "shipped", "cancelled"]
    amount: float = Field(ge=0)

try:
    Order(order_id=1, status="lost", amount=-5)
except ValidationError as exc:
    for e in exc.errors():
        print(e["loc"], e["type"])
```

`Literal` is `accepted_values`; `Field(ge=0)` is a `CHECK (amount >= 0)`. Note that **all** the problems are reported, not only the first.

## Validators: custom cleaning

Use `field_validator` for rules the type cannot express. `mode="before"` runs on the raw input, before type conversion, which is where you strip `$` signs:

```python
from pydantic import BaseModel, field_validator

class Line(BaseModel):
    customer: str
    amount: float

    @field_validator("customer")
    @classmethod
    def tidy_name(cls, value: str) -> str:
        return value.strip().title()

    @field_validator("amount", mode="before")
    @classmethod
    def money(cls, value):
        if isinstance(value, str):
            return value.replace("$", "").replace(",", "").strip()
        return value

print(Line(customer="  ada LOVELACE ", amount="$1,234.50"))
```

A validator **must return the value**. If you forget the `return`, the field silently becomes `None`: the most common validator bug.

## Parsing a row into a typed object

The idiom: dict in, typed object out, in one place, with a clear failure.

```python
import csv, io
from datetime import date
from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: int
    email: str
    signup_date: date

text = "customer_id,email,signup_date\n1,a@x.com,2024-06-12\n2,b@x.com,2025-03-29\n"
customers = [Customer.model_validate(row) for row in csv.DictReader(io.StringIO(text))]
print(customers[0])
print(customers[1].signup_date.year)
```

Everything after this point works with real `int` and `date` values and attribute access (`c.email`), with editor autocomplete and type checking, not stringly-typed dictionaries.

## Common mistakes

- `pydantic_core._pydantic_core.ValidationError: 1 validation error for Row ... Input should be a valid integer, unable to parse string as an integer`: the data is bad, not the code. Catch it where you can decide what to do (next lesson).
- Validator without `return`: the field becomes `None` and a later step fails mysteriously.
- Forgetting `@classmethod` under `@field_validator`.
- Assuming extra keys are an error: by default they are silently ignored. Use `ConfigDict(extra="forbid")` to catch unexpected columns.
- Using a mutable default like `tags: list = []` is safe in pydantic (copied per instance), but `Field(default_factory=list)` states the intent.

## What to take away

1. A `BaseModel` is a schema with constraints; `model_validate(row)` checks and converts in one step.
2. Lax mode converts sensible strings (CSV boundary); `strict=True` refuses conversion.
3. `Literal`, `Field(ge=...)` and friends are your `accepted_values` and `CHECK`s.
4. `field_validator` for cleaning; `mode="before"` sees raw input; always return the value.
5. `ValidationError.errors()` gives structured `loc`/`type`/`msg` for reports.
