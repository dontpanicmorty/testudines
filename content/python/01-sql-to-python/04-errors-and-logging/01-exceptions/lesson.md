+++
id = "errors-and-logging.exceptions"
title = "Exceptions"
minutes = 30
+++

# Exceptions

In SQL a bad cast fails the whole statement, unless you wrote `TRY_CAST`. Python errors are **exceptions**: objects that interrupt normal flow and travel up the call stack until something catches them, or the program dies with a traceback. Your job is to decide, at each layer, who should handle which failure.

> **SQL bridge.** `TRY_CAST(x AS INT)` returns NULL on failure. The Python equivalent is a `try`/`except ValueError` around `int(x)`. And `ON_ERROR = 'CONTINUE'` vs `'ABORT_STATEMENT'` in a load is the same decision you make with `except ... continue` vs letting it propagate.

## try / except

```python
def parse_qty(text):
    try:
        return int(text)
    except ValueError:
        return None

print(parse_qty("12"), parse_qty("twelve"), parse_qty(""))
```

Catch the **specific** exception you expect. A bare `except:` or `except Exception:` hides real bugs: a typo in a variable name (`NameError`) would be swallowed and reported as "bad quantity".

> **Predict first.** What does this print, and why is it a bad idea?

```python
def parse_qty(text):
    try:
        return int(txt)        # typo
    except Exception:
        return None

print(parse_qty("12"))
```

It prints `None` for perfectly valid input. The bug is invisible. Catch `ValueError` and the typo would have crashed loudly with `NameError: name 'txt' is not defined`, which is exactly what you want during development.

You can catch several types and bind the exception to a name:

```python
import json

for text in ['{"a": 1}', "{bad", None]:
    try:
        print(json.loads(text))
    except json.JSONDecodeError as e:
        print("bad json:", e.msg)
    except TypeError as e:
        print("not text:", e)
```

## else and finally

- `else` runs only if the `try` block raised nothing. Put the code that depends on success there, so the `try` body stays tiny.
- `finally` always runs: success, failure, even `return`. Use it for cleanup (though `with` handles most of that).

```python
def load(text):
    try:
        value = int(text)
    except ValueError:
        print("  bad value")
        return None
    else:
        print("  parsed ok")
        return value
    finally:
        print("  done with", repr(text))

print(load("5"))
print(load("x"))
```

Keep the `try` body to the one line that can fail. The wider the body, the more unrelated errors you accidentally catch.

## Raising

Detecting a problem you cannot fix locally? `raise` it.

```python
def discount(price, pct):
    if not 0 <= pct <= 100:
        raise ValueError(f"pct must be between 0 and 100, got {pct}")
    return price * (100 - pct) / 100

try:
    discount(50, 120)
except ValueError as e:
    print("rejected:", e)
```

Pick the built-in that fits: `ValueError` (right type, bad value), `TypeError` (wrong type), `KeyError`, `FileNotFoundError`. Write messages that include the offending **value** and what was expected.

A bare `raise` inside `except` re-raises the current exception unchanged, handy after logging.

## Custom exceptions

When callers need to react to *your* failures, define a class. Subclass `Exception`.

```python
class PipelineError(Exception):
    """Base class for errors raised by our pipeline."""

class SchemaError(PipelineError):
    def __init__(self, missing):
        self.missing = sorted(missing)
        super().__init__(f"missing columns: {', '.join(self.missing)}")

def check_columns(header, required):
    missing = set(required) - set(header)
    if missing:
        raise SchemaError(missing)

try:
    check_columns(["id", "amount"], ["id", "amount", "currency", "region"])
except PipelineError as e:           # catches SchemaError too
    print(type(e).__name__, "->", e, e.missing)
```

A shared base class lets a caller say "handle anything from this library" with one `except`, while still allowing finer handlers.

## Chaining with `from`

Wrapping a low-level error in a domain error should not lose the original cause.

```python
class LoadError(Exception):
    pass

def load_amount(raw):
    try:
        return float(raw)
    except ValueError as e:
        raise LoadError(f"invalid amount {raw!r}") from e

try:
    load_amount("$5")
except LoadError as e:
    print(e)
    print("caused by:", repr(e.__cause__))
```

The traceback will show both, joined by "The above exception was the direct cause of the following exception". Without `from e` you get the confusing "During handling of the above exception, another exception occurred". Use `from None` only when you deliberately want to hide the cause.

## Where to catch

Catch where you can **do something useful**: retry, skip a row, substitute a default, or translate into a domain error. If you cannot, let it propagate. Catching, printing and carrying on with garbage is the worst outcome: the pipeline "succeeds" and produces wrong data.

## Common mistakes

- `except:` or `except Exception: pass` swallowing everything.
- `KeyError: 'amount'` where a `.get` default would hide a real schema break. Decide which you want.
- Raising bare strings: `TypeError: exceptions must derive from BaseException`.
- Re-raising a new exception without `from`, losing the root cause.

## What to take away

1. Catch specific exceptions around the smallest possible `try` body.
2. `else` for success-only code, `finally` for cleanup.
3. `raise` built-ins with messages that include the bad value.
4. Custom exceptions share a base class so callers can choose their granularity.
5. Chain with `raise New(...) from err`.
