+++
id = "capstones.capstone-shared-library"
title = "Capstone: a shared library"
minutes = 90
+++

# Capstone: a shared library

Every team ends up with a `utils.py` that grows by copy-paste until nobody dares change it. This capstone is the opposite: design a small library, **`datakit`**, as if other teams will depend on it. The difference between a pile of helpers and a library is not the code, it is the **contract**: what you promise not to break.

> **SQL bridge.** A dbt package or a shared macro library works the same way. Consumers call `{{ my_package.safe_divide(a, b) }}` and expect it to keep working next quarter. Renaming an argument is a breaking change even if the new name is "better".

## The brief

Build a package with five parts:

1. **Typed config loader**: turn environment variables into a dataclass with real types and clear errors.
2. **Retry decorator**: re-run flaky calls with exponential backoff.
3. **Row validator**: describe rules once, split rows into valid and invalid with reasons.
4. **`ConnectionProtocol`** plus a **sqlite implementation**: code depends on the *shape* of a connection, not on a specific database.
5. A deliberately small **public API**, guarded by tests.

## Layout

```text
datakit/
  __init__.py   the public surface: imports + __all__ + __version__
  errors.py     DatakitError, ConfigError, DatabaseError
  config.py     load_config
  retry.py      retry
  validate.py   RowValidator
  db.py         ConnectionProtocol, SqliteConnection
```

Consumers write `from datakit import retry`. They never import `datakit.retry`, so you stay free to reorganise files inside. Anything not in `__all__` is private by agreement.

## Design decisions to think through

**A decorator factory has three layers.** `@retry(attempts=3)` first *calls* `retry(...)`, which returns the real decorator, which wraps your function. `functools.wraps` copies the original's name and docstring so tracebacks and help still make sense:

```python
import functools

def shout(times):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs).upper() * times
        return wrapper
    return decorator

@shout(2)
def greet(name):
    """Say hello."""
    return f"hi {name} "

print(greet("ada"), greet.__name__, greet.__doc__)
```

**Make time injectable.** A retry that really sleeps makes tests slow. Take `sleep=time.sleep` as a parameter and tests pass `sleeps.append` to record the delays instead. The default keeps real behaviour; the seam keeps tests instant.

**Report every config problem at once.** Failing on the first missing variable means a deploy takes five attempts to find five mistakes. Collect all errors, raise once:

```python
import dataclasses
import typing

@dataclasses.dataclass
class Settings:
    db_path: str
    max_rows: int = 100

def check(cls, env):
    problems = []
    hints = typing.get_type_hints(cls)
    for f in dataclasses.fields(cls):
        key = f.name.upper()
        if key not in env and f.default is dataclasses.MISSING:
            problems.append(f"{key}: missing")
        elif key in env and hints[f.name] is int and not env[key].strip().lstrip("-").isdigit():
            problems.append(f"{key}: cannot parse {env[key]!r} as int")
    return problems

print(check(Settings, {"MAX_ROWS": "lots"}))
```

**Protocols over base classes.** A `typing.Protocol` describes the methods a connection must have. Anything with those methods qualifies, with no inheritance. That is why a consumer can pass a fake in tests, and why you can add a DuckDB implementation later without touching callers:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Greeter(Protocol):
    def greet(self) -> str: ...

class English:
    def greet(self) -> str:
        return "hello"

class Silent:
    pass

print(isinstance(English(), Greeter), isinstance(Silent(), Greeter))
```

`runtime_checkable` lets `isinstance` check that the methods *exist* (not their signatures).

**Your own exception hierarchy.** Wrap lower-level errors (`sqlite3.Error`) in your own `DatabaseError` using `raise DatabaseError(...) from exc`. Callers catch `DatakitError` without caring which driver you use, and the original is still available as `__cause__`.

**Treat the public API as a promise.** `test_public_api.py` pins the exported names, parameter names and defaults, keyword-only markers and the exception hierarchy. When one of those tests fails, the question is not "how do I make the test pass" but "am I willing to ship a breaking change (a new major version)?" Additions are safe; renames and removals are not.

## How to work

1. Read the prompt's API section end to end; write `__init__.py` with the exports first.
2. Implement `config.py`, `retry.py`, `validate.py` independently; each has its own test file.
3. Implement `db.py`, including the nested-transaction rule.
4. Run **Check** and read failures as a consumer: "I called it this way, it should have done that."
5. Finish by reading `test_public_api.py` slowly; it is the part that makes this a library.

## Common mistakes

- **Mutable default arguments** such as `exceptions=[...]` shared by every call.
- **Forgetting `functools.wraps`**: every decorated function is then named `wrapper`.
- **Catching `Exception` in the retry loop** when the caller listed specific exceptions.
- **Swallowing the original exception** after the last attempt, or raising a new generic one.
- **Exporting everything**: whatever you export you must support forever.
- **`print` for diagnostics in a library**; use `logging` so consumers control output.

## What to take away

1. A library is a contract: small public surface, stable names, explicit versioning.
2. Decorator factories are three nested functions; use `functools.wraps`.
3. Inject time and connections so tests are fast and fakes are easy.
4. Protocols describe shape, not ancestry.
5. Own your exceptions, chain the originals, and guard the public API with tests.
