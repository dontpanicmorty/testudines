+++
id = "classes-dataclasses-typing.dataclasses"
title = "Dataclasses"
minutes = 30
+++

# Dataclasses

Last lesson you wrote `__init__` and `__repr__` by hand. For classes that mostly *hold fields*, that is boilerplate. The `@dataclass` decorator writes it for you from a list of annotated fields.

> **SQL bridge.** A dataclass is a row type: a declared list of columns with types and defaults, like a `CREATE TABLE` or one entry in a dbt `schema.yml`. `frozen=True` is a row that can't be `UPDATE`d.

## From boilerplate to one decorator

```python
class ColumnSpecManual:
    def __init__(self, name, dtype, nullable=True):
        self.name = name
        self.dtype = dtype
        self.nullable = nullable

    def __repr__(self):
        return f"ColumnSpecManual(name={self.name!r}, dtype={self.dtype!r}, nullable={self.nullable!r})"

    def __eq__(self, other):
        return (self.name, self.dtype, self.nullable) == (other.name, other.dtype, other.nullable)

from dataclasses import dataclass

@dataclass
class ColumnSpec:
    name: str
    dtype: str
    nullable: bool = True

c = ColumnSpec("order_id", "int", nullable=False)
print(c)
print(c == ColumnSpec("order_id", "int", False))
```

The decorator generates `__init__`, `__repr__` and `__eq__` from the annotations. The annotations *are* the field declarations. (They also act as documentation; the type checker lesson will use them properly.)

Fields without a default must come before fields with one, just like function parameters.

## Defaults and the mutable-default trap

```python
from dataclasses import dataclass, field

@dataclass
class Table:
    name: str
    columns: list[str] = field(default_factory=list)
    row_count: int = 0

a, b = Table("orders"), Table("customers")
a.columns.append("order_id")
print(a.columns, b.columns)
```

`field(default_factory=list)` builds a *new* list for each instance. Writing `columns: list[str] = []` is the shared-class-attribute bug from last lesson, and dataclasses refuse it outright with `ValueError: mutable default <class 'list'> for field columns is not allowed: use default_factory`. Use `default_factory` for lists, dicts and sets.

## Validation with `__post_init__`

After the generated `__init__` has stored the fields, Python calls `__post_init__` if you define it. That is the place to validate or normalise:

```python
from dataclasses import dataclass

@dataclass
class Loan:
    principal: float
    rate: float

    def __post_init__(self):
        if self.principal <= 0:
            raise ValueError(f"principal must be positive, got {self.principal}")
        if not 0 <= self.rate <= 1:
            raise ValueError(f"rate must be between 0 and 1, got {self.rate}")

print(Loan(1000, 0.05))
try:
    Loan(-5, 0.05)
except ValueError as exc:
    print("rejected:", exc)
```

Making invalid states impossible to construct means every function receiving a `Loan` can trust it. Validate at the boundary once, trust inside.

## Frozen: immutable records

`@dataclass(frozen=True)` blocks assignment after creation, and makes instances hashable (usable as dict keys or in sets). Use it for values that shouldn't change: keys, events, configuration.

```python
from dataclasses import dataclass, replace, FrozenInstanceError

@dataclass(frozen=True)
class Event:
    user_id: int
    name: str

e = Event(1, "login")
try:
    e.name = "logout"
except FrozenInstanceError as exc:
    print("blocked:", type(exc).__name__)

e2 = replace(e, name="logout")      # make a modified copy
print(e, e2, len({e, e2, Event(1, "login")}))
```

To normalise inside a frozen class's `__post_init__`, assign with `object.__setattr__(self, "name", value)`; the one sanctioned escape hatch.

## Ordering and conversion

`order=True` generates `<`, `>` and friends comparing fields in order, so instances sort:

```python
from dataclasses import dataclass, asdict

@dataclass(order=True)
class Version:
    major: int
    minor: int = 0

print(sorted([Version(1, 10), Version(1, 9), Version(0, 5)]))
print(asdict(Version(2, 3)))
```

Because the comparison is numeric on each field, `1.10 > 1.9`, unlike comparing strings. `asdict` converts to a plain dict, handy for JSON or building DataFrame rows.

## Dataclass, dict, or Pydantic?

- Internal, trusted records: **dataclass**.
- Untrusted input (JSON, API payloads) that needs parsing and type coercion: **Pydantic** (later stage). A dataclass doesn't convert `"5"` into `5`.
- Throwaway shape with unknown keys: a dict.

## Common mistakes

- `columns: list[str] = []`, which raises the `ValueError` shown above. Use `field(default_factory=list)`.
- A field without default after one with a default: `TypeError: non-default argument 'name' follows default argument`.
- Expecting the annotations to enforce types at runtime. `Loan("abc", 0.1)` constructs fine unless you validate in `__post_init__`.
- Mutating a frozen instance, giving `FrozenInstanceError: cannot assign to field 'name'`. Use `replace(obj, name=...)`.
- Using `order=True` on a class whose field order isn't the order you'd sort by.

## What to take away

1. `@dataclass` generates `__init__`, `__repr__` and `__eq__` from annotated fields.
2. Mutable defaults need `field(default_factory=...)`.
3. `__post_init__` is where validation and normalisation belong.
4. `frozen=True` gives immutable, hashable records; `replace` makes modified copies.
5. `order=True` makes instances sortable field by field.
