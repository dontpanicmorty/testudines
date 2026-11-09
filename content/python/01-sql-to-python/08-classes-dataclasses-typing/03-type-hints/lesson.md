+++
id = "classes-dataclasses-typing.type-hints"
title = "Type hints and mypy"
minutes = 35
+++

# Type hints and mypy

In Snowflake and dbt, types are enforced for you: insert text into an `INT` column and the warehouse refuses. dbt **model contracts** go further and fail the build if a model's columns drift from the declared types. Python's equivalent is **type hints** plus a checker called **mypy**. The hints don't change how code runs; the checker reads them and finds contradictions before you run anything.

> **SQL bridge.** `CREATE TABLE t (id INT NOT NULL, note VARCHAR)` → `id: int`, `note: str | None`. A dbt contract check → `python -m mypy`.

## Annotating functions

Put the type after a colon for parameters, and after `->` for the return value:

```python
def total_cents(prices: list[float]) -> int:
    return sum(round(p * 100) for p in prices)

def greet(name: str, excited: bool = False) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"

print(total_cents([1.10, 2.20]), greet("Ada"))
```

Python itself ignores these, so `total_cents("oops")` still runs (and crashes). The value comes from mypy catching that mistake *without running it*. A function that returns nothing is `-> None`.

## Containers and "or None"

```python
rows: list[dict[str, str]] = [{"id": "1"}]     # list of dicts of str -> str
prices: dict[str, float] = {"pen": 1.5}        # mapping
pair: tuple[int, str] = (1, "a")               # fixed-length, mixed types
ids: set[int] = {1, 2}
maybe_name: str | None = None                  # a str, or None (like a nullable column)

def find_price(name: str) -> float | None:
    return prices.get(name)

print(find_price("pen"), find_price("nope"))
```

`X | None` (older code writes `Optional[X]`) is the type-system version of a nullable column. Its power: mypy then *forces you to handle the None* before using the value:

```python
# no-run
def shout(name: str | None) -> str:
    return name.upper()          # mypy: Item "None" of "str | None" has no attribute "upper"

def shout_ok(name: str | None) -> str:
    if name is None:
        return ""
    return name.upper()          # fine: mypy knows name is a str here
```

That narrowing after an `is None` check is how most Optional bugs get fixed.

## Running mypy

Mypy is a command (`python -m mypy file.py`). Here is a helper that runs it on a snippet so you can read real messages:

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def run_mypy(source):
    folder = Path(tempfile.mkdtemp())
    (folder / "snippet.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "mypy", "--no-incremental",
           "--cache-dir", str(folder / ".cache"), "snippet.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print(r.stdout.strip())

run_mypy('''
def mean(values: list[float]) -> float:
    return sum(values) / len(values)

mean("12")
total: int = mean([1.0, 2.0])

def find(name: str, rows: dict[str, int]) -> int:
    return rows.get(name)
''')
```

Read each message as `file:line: error: <what>  [error-code]`. The three above are typical: a wrong argument type, assigning a `float` to an `int` variable, and returning `int | None` where `int` was promised (`dict.get` can return None, exactly the nullable-column issue).

Add `--strict` to demand annotations everywhere; a good setting for new code. You can also put settings in `pyproject.toml` under `[tool.mypy]`.

## Running mypy mentally

Before you press enter, scan for these four things:

1. Every parameter and return has a type?
2. Anything that can be `None` (`.get`, `re.match`, optional params) is checked before use?
3. Do the declared return types match what each `return` actually gives, in every branch?
4. Do callers pass what the signature says?

## TypedDict: a dict with known keys

JSON rows are dicts, but a bare `dict[str, object]` says nothing about which keys exist. A `TypedDict` declares the keys and their types (it's like a one-row schema); at runtime it's still a plain dict.

```python
from typing import TypedDict

class Event(TypedDict):
    user_id: int
    name: str
    value: float

def describe(e: Event) -> str:
    return f"{e['name']} by user {e['user_id']}"

event: Event = {"user_id": 7, "name": "click", "value": 2.5}
print(describe(event), type(event))
```

mypy flags a missing key or a wrong value type when you build an `Event`.

## Protocol: "anything with these methods"

A **Protocol** describes an interface by shape. Any class with a matching method qualifies, with no inheritance needed. (This is called structural typing; it's duck typing that a checker can verify.)

```python
from typing import Protocol

class Sink(Protocol):
    def write(self, rows: list[dict[str, int]]) -> int: ...

class PrintSink:
    def write(self, rows: list[dict[str, int]]) -> int:
        for r in rows:
            print("row", r)
        return len(rows)

def load(rows: list[dict[str, int]], sink: Sink) -> int:
    return sink.write(rows)

print(load([{"a": 1}, {"a": 2}], PrintSink()))
```

`PrintSink` never mentions `Sink`, yet it is accepted because it has a `write` with the right signature. This is how you make code swappable (more in the last lesson of this module).

## Generics, lightly

Sometimes the output type depends on the input type. A **type variable** captures that relationship:

```python
def first_or_none[T](items: list[T]) -> T | None:
    return items[0] if items else None

n = first_or_none([10, 20])      # mypy infers: int | None
s = first_or_none(["a", "b"])    # mypy infers: str | None
print(n, s, first_or_none([]))
```

`[T]` after the name is the modern (Python 3.12) syntax; older code uses `TypeVar("T")`. You will mostly *use* generic types (`list[int]`, `dict[str, float]`) rather than write generic functions.

## Common mistakes

- `Incompatible return value type (got "int | None", expected "int")`: you forgot that `dict.get` can return `None`. Check it, or change the return type.
- `Need type annotation for "groups"`: mypy can't infer an empty `{}`. Annotate: `groups: dict[str, list[str]] = {}`.
- Silencing errors with `# type: ignore` instead of fixing the cause. Use it only with a reason, and rarely.
- Using `Any` to make errors disappear. It switches checking off for everything it touches.
- Believing hints are enforced at runtime. They aren't; only the checker (and tools like Pydantic) enforce them.

## What to take away

1. Hints are labels for a checker; Python ignores them at runtime.
2. `X | None` models nullable values, and mypy makes you handle the None.
3. Use `list[...]`, `dict[..., ...]`, `tuple[...]` to describe containers.
4. `TypedDict` describes dict rows; `Protocol` describes an interface by shape.
5. `python -m mypy --strict` finds contradictions before you run the code. Read its `file:line: error` messages like a failing test.
