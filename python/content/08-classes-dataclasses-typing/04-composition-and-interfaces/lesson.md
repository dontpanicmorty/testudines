+++
id = "classes-dataclasses-typing.composition-and-interfaces"
title = "Composition and interfaces"
minutes = 35
+++

# Composition and interfaces

A dbt model doesn't care whether `source('crm', 'customers')` is a Snowflake table or a seed, and you can point the same project at a different warehouse by changing the target. The model's logic is separate from where data lives. This lesson is about writing Python the same way: components that you can **swap** without touching the logic.

> **SQL bridge.** `source()` and `target` are interfaces: the model depends on "something that provides rows", not on a specific system. Adapters (Snowflake, DuckDB, Postgres) are interchangeable implementations.

## Inheritance versus composition

Two ways to reuse behaviour:

- **Inheritance** ("is-a"): `class CsvLoader(BaseLoader)` inherits everything from `BaseLoader`.
- **Composition** ("has-a"): a `Pipeline` *holds* a source and a sink and calls them.

Inheritance couples you tightly to the parent's internals, and chains of it get hard to follow. The rule of thumb: **prefer composition**, and use inheritance only for a true "is-a" with a small, stable interface.

Here is the trap in the naive inheritance version:

```python
class Loader:
    def __init__(self):
        self.count = 0

    def load(self, rows):
        for row in rows:
            self.write(row)
            self.count += 1

class PrintLoader(Loader):
    def write(self, row):
        print("write", row)

class CsvLoader(Loader):
    def __init__(self, path):
        self.path = path              # forgot super().__init__() ...

    def write(self, row):
        print("csv", row)

p = PrintLoader()
p.load([1, 2])
print(p.count)

try:
    CsvLoader("x.csv").load([1])
except AttributeError as exc:
    print("error:", exc)
```

The subclass silently depends on parent state it forgot to set up. Compose instead and the dependency is explicit.

## Interfaces: the two ways to say "I need something that can..."

An **abstract base class** (ABC) defines methods that subclasses must provide; instantiating one that doesn't raises an error immediately:

```python
from abc import ABC, abstractmethod

class Sink(ABC):
    @abstractmethod
    def write(self, rows: list[dict]) -> int:
        """Persist rows; return how many were written."""

class MemorySink(Sink):
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def write(self, rows: list[dict]) -> int:
        self.rows.extend(rows)
        return len(rows)

class Broken(Sink):
    pass

print(MemorySink().write([{"a": 1}]))
try:
    Broken()
except TypeError as exc:
    print("error:", exc)
```

A `Protocol` (last lesson) says the same thing by shape, with no inheritance required. Use an **ABC** when you also want shared helper code or enforcement at instantiation; use a **Protocol** when you want the lightest contract, especially for code you don't control.

## The strategy pattern

A **strategy** is a swappable piece of behaviour passed in as a parameter. In Python the lightest strategy is simply a function:

```python
def keep_first(group):
    return group[0]

def keep_last(group):
    return group[-1]

def dedupe(rows, key, strategy):
    groups = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    return [strategy(g) for g in groups.values()]

rows = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
print(dedupe(rows, "id", keep_first))
print(dedupe(rows, "id", keep_last))
```

`dedupe` doesn't know or care *how* to choose, so adding `keep_max_by("updated_at")` later touches nothing else. Reach for a class only when the strategy needs its own state or several related methods.

## Extract, transform, load as composed parts

Now put it together. A pipeline **has** a source, a transformation and a sink. Each part is replaceable, and tests can use in-memory versions of the I/O ends.

```python
from dataclasses import dataclass
from typing import Callable, Iterable, Protocol

class Sink(Protocol):
    def write(self, rows: list[dict]) -> int: ...

@dataclass(frozen=True)
class RunResult:
    rows_in: int
    rows_out: int
    rejected: int

class Pipeline:
    def __init__(self, extract: Callable[[], Iterable[dict]],
                 transform: Callable[[dict], dict | None],
                 sink: Sink) -> None:
        self.extract = extract
        self.transform = transform
        self.sink = sink

    def run(self) -> RunResult:
        raw = list(self.extract())
        good = [out for r in raw if (out := self.transform(r)) is not None]
        written = self.sink.write(good)
        return RunResult(len(raw), written, len(raw) - len(good))

class ListSink:
    def __init__(self) -> None:
        self.rows: list[dict] = []
    def write(self, rows: list[dict]) -> int:
        self.rows.extend(rows)
        return len(rows)

def only_positive(row: dict) -> dict | None:
    return {**row, "amount": abs(row["amount"])} if row["amount"] > 0 else None

sink = ListSink()
result = Pipeline(lambda: [{"amount": 5}, {"amount": -1}, {"amount": 2}], only_positive, sink).run()
print(result)
print(sink.rows)
```

Replace `lambda: [...]` with a CSV reader and `ListSink` with a warehouse writer and the `Pipeline` class doesn't change. That separation is also why it is easy to test.

## Choosing

| Need | Tool |
|---|---|
| Swap one behaviour (how to dedupe, how to retry) | Pass a function |
| Define "anything with a `write` method" | `Protocol` |
| Enforce a contract plus share helper code | ABC |
| Reuse by combining components | Composition (hold them as attributes) |
| True "is-a" with stable base | Inheritance, sparingly |

## Common mistakes

- Deep class hierarchies for reuse. Compose smaller parts.
- Subclass forgets `super().__init__()` and fails later with `AttributeError: 'CsvLoader' object has no attribute 'count'`.
- `TypeError: Can't instantiate abstract class Broken without an implementation for abstract method 'write'`: the subclass didn't implement every abstract method.
- Hard-coding the concrete sink inside `Pipeline` (`self.sink = SnowflakeSink()`) so it can't be tested without a warehouse. Pass it in.
- Writing a class for something a function does.

## What to take away

1. Prefer composition ("has-a") to inheritance ("is-a").
2. Define interfaces with `Protocol` (shape) or `ABC` (enforced base).
3. A strategy is a swappable behaviour, usually just a function argument.
4. Build pipelines from an extract, a transform and a sink that you pass in.
5. Passing dependencies in is what makes code testable and swappable.
