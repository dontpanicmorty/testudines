+++
id = "shared-libraries.evolving-without-breaking"
title = "Evolving without breaking consumers"
minutes = 35
+++

# Evolving without breaking consumers

Renaming a column in a widely used dbt model is a breaking change: every downstream model and dashboard that selects it fails. Mature teams add the new column, keep the old one for a while, announce the removal, then delete it. Libraries work the same way, with better tooling for the middle step.

> **dbt bridge.** Model contracts and `deprecation_date` in a model's YAML exist for exactly this: promise a shape, warn before removal. Python's equivalents are signature rules, `warnings.warn`, and contract tests.

## Breaking or not?

A change is **breaking** if code that worked before can fail or behave differently after. Look at it from the caller's side.

| Change | Breaking? |
|---|---|
| Add optional keyword parameter (default keeps old behaviour) | no |
| Add a new function | no |
| Add a required parameter | **yes** |
| Rename or remove a parameter or function | **yes** |
| Reorder positional parameters | **yes** |
| Make a positional-or-keyword parameter keyword-only | **yes** |
| Return a different type or change a column order | **yes** |
| Raise an exception where it used to return | usually **yes** |

> **Predict first.** `def load(path)` becomes `def load(path, strict=True)` and strict now raises on bad rows, where it used to skip them. Breaking?

Yes, even though the signature is compatible. Behaviour is part of the contract. The safe version defaults `strict=False` to preserve old behaviour.

You can inspect signatures programmatically, which is how automated API-diff tools work:

```python
import inspect

def v1(path, delimiter=","): ...
def v2(path, delimiter=",", *, encoding="utf-8"): ...   # compatible
def v3(path, *, delimiter=","): ...                       # breaking

for fn in (v1, v2, v3):
    print(fn.__name__, inspect.signature(fn))
    for name, p in inspect.signature(fn).parameters.items():
        print("   ", name, p.kind.name, "default" if p.default is not p.empty else "required")
```

## Deprecation with warnings.warn

To rename, keep the old name, make it call the new one, and **warn**. Consumers see the message in their test runs and can migrate on their schedule.

```python
import warnings

def load_rows(path):
    return [f"row from {path}"]

def read_rows(path):
    """Deprecated alias for load_rows."""
    warnings.warn(
        "read_rows is deprecated, use load_rows instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return load_rows(path)

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    print(read_rows("a.csv"))
print([str(w.message) for w in caught], caught[0].category.__name__)
```

Two details matter. `DeprecationWarning` is the category for "will be removed". `stacklevel=2` attributes the warning to the **caller's** line, not to your library's, which is the code the consumer must change.

Python hides `DeprecationWarning` by default outside of `__main__` and test runners, so tell consumers to run their tests with warnings enabled (pytest shows them).

A reusable decorator removes the repetition:

```python
import functools
import warnings

def deprecated(use_instead):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{fn.__name__} is deprecated, use {use_instead}",
                DeprecationWarning,
                stacklevel=2,
            )
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@deprecated("new_total")
def total(xs):
    return sum(xs)

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    print(total([1, 2, 3]), w[0].message)
```

State the removal version in the message and the changelog ("removed in 2.0.0"). Remove only at a major release.

## Backward-compatible behaviour changes and feature flags

When a fix changes output, ship the new behaviour behind an opt-in, make it the default in the next major version, and remove the flag later.

```python
import os

def flag_enabled(name, environ=None):
    environ = os.environ if environ is None else environ
    return environ.get(f"DATAKIT_{name.upper()}", "").lower() in {"1", "true", "yes"}

def round_amount(x, environ=None):
    if flag_enabled("banker_rounding", environ):
        return round(x)          # banker's rounding: 2.5 -> 2
    return int(x + 0.5)          # legacy: 2.5 -> 3

print(round_amount(2.5, {}), round_amount(2.5, {"DATAKIT_BANKER_ROUNDING": "1"}))
```

Flags are temporary scaffolding. Each one doubles the paths you must test; write down when it will be deleted.

## Contract tests

A **contract test** pins the behaviour consumers rely on: given these inputs, expect these outputs, and the function accepts these call shapes. Keep them separate from your internal unit tests and **never edit them casually**: if one fails, you have found a breaking change.

```python
def summarize(rows, key, *, top_n=None):
    counts = {}
    for r in rows:
        counts[r[key]] = counts.get(r[key], 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked if top_n is None else ranked[:top_n]

CONTRACT = [
    (([{"a": 1}, {"a": 1}], "a"), {}, [(1, 2)]),
    (([{"a": 1}, {"a": 2}, {"a": 2}], "a"), {"top_n": 1}, [(2, 2)]),
]
for args, kwargs, expected in CONTRACT:
    got = summarize(*args, **kwargs)
    print("ok" if got == expected else f"BROKEN: {got}")
```

Real teams go one step further and run the **consumers'** own tests against a release candidate.

## Common mistakes

- Deprecating without `stacklevel=2`: the warning points inside your library and nobody can find their call.
- Removing a deprecated function in a minor release.
- Behaviour changes hidden in a patch release.
- Writing the warning text without saying what to use instead.

## What to take away

1. Judge breaking changes from the caller's side, including behaviour and exceptions.
2. Additions are safe if optional and keyword-only; renames and removals are not.
3. Deprecate first with `warnings.warn(..., DeprecationWarning, stacklevel=2)`, remove at a major release.
4. Use temporary feature flags to introduce new behaviour.
5. Contract tests pin what consumers rely on.
