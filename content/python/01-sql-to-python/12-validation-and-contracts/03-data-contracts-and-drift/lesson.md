+++
id = "validation-and-contracts.data-contracts-and-drift"
title = "Data contracts and schema drift"
minutes = 30
+++

# Data contracts and schema drift

Your upstream team renames `cust_id` to `customer_id` on a Friday. Monday's dashboards are empty. A **data contract** is an explicit, versioned statement of what a dataset looks like, plus a check that fails *loudly* when reality stops matching. You already use these ideas in dbt: `contract: enforced: true` on a model pins column names and types, and tests such as `not_null` and `accepted_values` check the data. Here you build the same mechanisms in Python, so they can guard files, API responses and the output of your own code.

> **SQL bridge.** A contract is the column list and types in a dbt model's YAML. Drift detection is the diff between yesterday's `INFORMATION_SCHEMA.COLUMNS` and today's.

## A schema as plain data

The simplest contract is a dict from column name to type name:

```python
CONTRACT = {"customer_id": "int", "email": "str", "plan": "str", "mrr": "float"}
print(CONTRACT)
```

It is data, so you can store it in a file, diff it in git and compare it in code. Contracts written as code or config get reviewed; contracts that live in someone's head get broken.

## Contract from a pydantic model

If you already have a model, derive the contract instead of writing it twice:

```python
from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: int
    email: str
    plan: str
    mrr: float = 0.0

contract = {name: field.annotation.__name__ for name, field in Customer.model_fields.items()}
print(contract)
```

`model_fields` is the model's own description of itself. One source of truth: change the model and the contract changes with it.

## Inferring a schema from observed data

To check what actually arrived, infer a schema from the rows:

```python
def infer_schema(rows: list[dict]) -> dict[str, str]:
    seen: dict[str, set[str]] = {}
    for row in rows:
        for column, value in row.items():
            seen.setdefault(column, set())
            if value is not None:
                seen[column].add(type(value).__name__)
    schema = {}
    for column, types in seen.items():
        if not types:
            schema[column] = "null"
        elif len(types) == 1:
            schema[column] = next(iter(types))
        elif types == {"int", "float"}:
            schema[column] = "float"
        else:
            schema[column] = "str"
    return schema

rows = [{"id": 1, "mrr": 10, "note": None}, {"id": 2, "mrr": 12.5, "note": None, "new": "x"}]
print(infer_schema(rows))
```

Notice the decisions: `int` mixed with `float` widens to `float`, an all-`None` column is `"null"`, anything else mixed becomes `"str"`. Every inference function has rules like these; write them down.

## Detecting drift

Compare two schemas and classify the differences:

```python
def diff_schemas(old: dict[str, str], new: dict[str, str]) -> dict:
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "retyped": {c: (old[c], new[c]) for c in sorted(old.keys() & new.keys()) if old[c] != new[c]},
    }

old = {"id": "int", "email": "str", "mrr": "int"}
new = {"id": "int", "mail": "str", "mrr": "float", "plan": "str"}
print(diff_schemas(old, new))
```

`removed: ['email']` plus `added: ['mail']` is a rename in disguise: to a program it is a removal and an addition. Humans notice the pattern; code can only report both.

> **Predict first.** Which of these changes would break a consumer that reads `email` and `mrr`: adding `plan`, removing `email`, changing `mrr` from int to float?

Removing `email` breaks it for sure. Adding `plan` does not. `int` to `float` is a *widening*: values stay valid for anyone reading numbers, so it is normally safe. `float` to `int` or anything to `str` is not.

## Backward compatibility and versions

A change is **backward compatible** when every consumer written against the old contract still works. A workable rule set:

- adding a column: compatible
- widening `int` to `float`: compatible
- removing a column: **breaking**
- any other type change: **breaking**

Semantic versioning maps onto it: breaking changes bump the **major** number, compatible additions bump the **minor**, no change keeps the version.

```python
def bump(version: str, kind: str) -> str:
    major, minor, patch = (int(p) for p in version.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return version

print(bump("1.4.2", "major"), bump("1.4.2", "minor"), bump("1.4.2", "none"))
```

Publish the version with the contract. A consumer can pin `>=1,<2` and trust that nothing breaking arrives without a major bump, the same promise a dbt model version makes.

## Checking rows against a contract

```python
CONTRACT = {"id": "int", "email": "str"}

def check_row(row: dict) -> list[str]:
    problems = []
    for column, type_name in CONTRACT.items():
        if column not in row:
            problems.append(f"missing {column}")
        elif row[column] is not None and type(row[column]).__name__ != type_name:
            problems.append(f"{column} is {type(row[column]).__name__}, expected {type_name}")
    problems += [f"unexpected {c}" for c in row if c not in CONTRACT]
    return problems

print(check_row({"id": 1, "email": "a@x"}))
print(check_row({"id": "1", "extra": 5}))
```

Checking is cheap, so run it on every batch, and decide in advance what each outcome means: *unexpected column* might be a warning, *missing column* or *wrong type* a hard stop.

## Where to enforce

- **At ingestion:** validate every row against the model (last lesson) and the batch against the contract (this lesson).
- **At publication:** before your own table is consumed, check that what you are about to write matches the version you promised.
- **In CI:** keep the contract file in git; a pull request that edits it shows reviewers exactly which consumers it can break.

## Common mistakes

- Detecting only type changes and missing the *rename* (removal plus addition).
- Comparing `type(v) is int` for booleans: `True` is an `int` subclass in Python, but `type(True).__name__` is `"bool"`. Use the exact type name when that matters.
- Inferring a schema from only the first row: a column that is `None` there looks like `"null"`.
- Treating every drift as an error: a new optional column is fine, and alert fatigue teaches people to ignore failures.
- No version on the contract, so nobody knows whether a change was announced.

## What to take away

1. A contract is explicit, versioned data: columns and types you promise.
2. Derive it from a model, or infer it from data, with written rules for mixed and null columns.
3. Drift = added, removed and retyped columns; a rename shows up as one removal and one addition.
4. Backward compatible: additions and widening are safe; removals and other retypes are breaking.
5. Map changes to semantic versions and check every batch before it reaches consumers.
