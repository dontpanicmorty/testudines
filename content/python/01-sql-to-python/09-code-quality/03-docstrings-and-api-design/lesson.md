+++
id = "code-quality.docstrings-and-api-design"
title = "Docstrings and API design"
minutes = 30
+++

# Docstrings and API design

In dbt every model and column has a `description:` and the docs site is generated from them. A **docstring** is the same thing for Python: documentation that lives *inside* the function, shown by `help()`, editors and doc generators. A function's name, signature, docstring and errors together form its **API**, the promise you make to everyone who calls it.

> **SQL bridge.** A column description in `schema.yml` and a model contract (declared columns and types) ≈ a docstring and a type-annotated signature. Breaking either is a breaking change for downstream users.

## What a docstring is

A string literal as the first statement of a function, class or module:

```python
def clean_email(raw: str) -> str | None:
    """Return the normalised e-mail address, or None if it is invalid."""
    value = raw.strip().lower()
    return value if "@" in value else None

print(clean_email.__doc__)
help(clean_email)
```

`help()` and your editor's hover tooltip display it. Write them in the **imperative** ("Return ...", not "Returns ..."), start with a one-line summary that fits on one line, then a blank line and details if needed.

## A convention for details

Pick one style per project. The widely used Google style lists arguments, return value and exceptions:

```python
def parse_duration(text: str) -> int:
    """Convert a compact duration such as ``"1h30m"`` into seconds.

    Args:
        text: Digits followed by a unit (``d``, ``h``, ``m`` or ``s``),
            optionally repeated.

    Returns:
        The total number of seconds.

    Raises:
        ValueError: If ``text`` is not a valid duration.

    Examples:
        >>> parse_duration("1h30m")
        5400
        >>> parse_duration("45s")
        45
    """
    units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    total, digits = 0, ""
    for ch in text.strip():
        if ch.isdigit():
            digits += ch
        elif ch in units and digits:
            total += int(digits) * units[ch]
            digits = ""
        else:
            raise ValueError(f"not a duration: {text!r}")
    if digits or not text.strip():
        raise ValueError(f"not a duration: {text!r}")
    return total

print(parse_duration("1h30m"), parse_duration("2d"))
```

The `Examples:` block with `>>>` is a **doctest**: Python can run it and check the printed output against what you wrote, so examples never silently go stale:

```python
import doctest

def double(n):
    """Return n doubled.

    >>> double(4)
    8
    >>> double(-1)
    -2
    """
    return n * 2

print(doctest.testmod())
```

`TestResults(failed=0, attempted=2)` means both examples ran and matched. With type hints in the signature, don't repeat the types in the docstring; describe meaning, units and constraints (`amount in cents, must be >= 0`).

## Design a small public API

Think of your module as a product with users. Principles:

1. **Small surface.** Export only what callers need. Name internals with a leading underscore (`_parse_line`) and list the public names in `__all__`.
2. **Obvious names**, consistent across the module: if one function is `read_orders`, don't call its sibling `load_customer_file`.
3. **Make the safe thing the default.** Required inputs first, optional ones with sensible defaults.
4. **Keyword-only for flags.** `load(path, *, strict=True)` forces callers to write `strict=False`; a bare `load(path, False)` is unreadable.
5. **Return values, don't print.** Library code returns or raises; callers decide what to do with the result.
6. **Type-hint the signature.** It is machine-checked documentation.

```python
__all__ = ["load_orders"]

def _parse_line(line: str) -> dict[str, str]:
    key, _, value = line.partition("=")
    return {key.strip(): value.strip()}

def load_orders(lines: list[str], *, strict: bool = True) -> list[dict[str, str]]:
    """Parse ``key=value`` lines into dicts.

    Args:
        lines: Raw text lines.
        strict: If true, raise ValueError on a line without ``=``; otherwise skip it.
    """
    rows = []
    for line in lines:
        if "=" not in line:
            if strict:
                raise ValueError(f"bad line: {line!r}")
            continue
        rows.append(_parse_line(line))
    return rows

print(load_orders(["a=1", "junk", "b = 2"], strict=False))
```

## Errors are part of the API

What your function does when things go wrong is as much a contract as what it returns. Decide on purpose:

- **Raise exceptions for failures; don't return error codes** like `-1` or `None` that callers forget to check. (Return `None` only when "no result" is a normal, documented outcome, such as a lookup that might miss.)
- Raise the **most specific built-in** that fits (`ValueError` for a bad value, `KeyError` for a missing key, `FileNotFoundError`...), or define your own.
- Make a **hierarchy** so callers can catch broadly or narrowly. Put the context in the message and in attributes.
- Chain with `raise ... from exc` to keep the original cause.

```python
class LoadError(Exception):
    """Base class for all errors raised by this library."""

class RowError(LoadError):
    def __init__(self, line_number: int, message: str) -> None:
        self.line_number = line_number
        super().__init__(f"line {line_number}: {message}")

try:
    raise RowError(3, "expected 2 fields, got 1")
except LoadError as exc:
    print(type(exc).__name__, "-", exc)
```

Callers who don't care which problem occurred catch `LoadError`; callers who do, catch `RowError` and read `exc.line_number`. Document each error in the docstring's `Raises:` section.

## Deprecations: changing an API kindly

Once others depend on a function you can't just delete it. Give notice with a **warning**, keep it working for a release or two, then remove it. `warnings.warn` with `stacklevel=2` points the warning at the *caller's* line, which is where they need to fix it:

```python
import warnings

def old_total(xs):
    warnings.warn("old_total is deprecated; use sum_values", DeprecationWarning, stacklevel=2)
    return sum(xs)

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    print(old_total([1, 2, 3]))

print(caught[0].category.__name__, "-", caught[0].message)
```

Say what to use instead, in the message and the docstring. Deprecation warnings are hidden by default outside test runs, which is why pytest shows them and why you should treat them as errors in CI.

## Common mistakes

- A docstring that repeats the name: `"""Clean the email."""` on `clean_email`. Say what it returns, and what counts as invalid.
- Documenting types that the signature already states, and then letting the two disagree.
- Returning `None` or `-1` for failure so callers silently carry bad data forward.
- `except Exception: pass` inside the library, swallowing the very information callers need.
- Changing a function's behaviour or argument order without warning.
- Positional boolean flags: `load(path, True, False)`.

## What to take away

1. A docstring starts with a one-line imperative summary; add `Args`, `Returns`, `Raises` as needed.
2. Put runnable examples in docstrings so they are checked.
3. Keep the public surface small: leading underscores plus `__all__`.
4. Use keyword-only arguments for flags and options.
5. Errors are part of the API: specific exceptions, a base class, useful messages, documented.
6. Deprecate with `warnings.warn(..., DeprecationWarning, stacklevel=2)` before removing anything.
