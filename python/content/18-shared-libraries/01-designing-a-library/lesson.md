+++
id = "shared-libraries.designing-a-library"
title = "Designing a library"
minutes = 30
+++

# Designing a library

Your dbt project has a macro package that three other projects install. Changing a macro's arguments breaks those projects, so you think carefully about what is public. A shared Python library is the same deal with more ways to go wrong.

> **dbt bridge.** A macro called from other projects is *public API*; a macro prefixed with an underscore is a private helper. Package consumers pin versions because you might rename things. Python gives you similar tools: naming conventions, `__all__`, and version numbers. This lesson is about deciding **what you promise**.

## Public versus private

Everything a consumer can import is a promise once they depend on it. Python has no hard access control, so the boundary is a convention everyone respects:

- a leading underscore (`_normalize`, `_internal.py`) means "private, may change without notice"
- anything else imported from the package top level is public

```python
# a library's internals, simulated in one file
def _normalize(name):          # private helper
    return " ".join(name.split()).title()

def clean_name(name):          # public function
    return _normalize(name)

print(clean_name("  ada   LOVELACE "))
```

If consumers import `_normalize`, they have broken the rules, but you will still hear about it when you change it. The best defence is a small public surface: easier to keep stable, easier to document.

## The package layout and `__all__`

A package is a directory with `__init__.py`. Users should import from the package top level, not from your internal module names, so you can reorganise files freely.

```
fmtkit/
    __init__.py      # the public face
    core.py          # implementation
    _text.py         # private helpers
```

`__init__.py` re-exports the public names and declares them in `__all__`:

```python
# fmtkit/__init__.py  # no-run
from fmtkit.core import clean_name, parse_amount

__all__ = ["clean_name", "parse_amount"]
```

`__all__` does two things: it is the documented list of public names, and it controls what `from fmtkit import *` brings in. Tools and linters also use it. You can see its effect with a throwaway module:

```python
import sys
import types

mod = types.ModuleType("demo")
exec(
    "def public(): return 1\n"
    "def other(): return 2\n"
    "__all__ = ['public']\n",
    mod.__dict__,
)
sys.modules["demo"] = mod

ns = {}
exec("from demo import *", ns)
print(sorted(k for k in ns if not k.startswith("__")))
```

## Keep dependencies light

Every dependency you add is imposed on every consumer, and a version conflict between your dependency and theirs is *their* problem. Ask:

- Can I do this with the standard library?
- Is the dependency needed for the whole library, or just one feature? If the latter, import it **inside the function** and make it optional (next lesson).
- A pure-Python core (no pandas, no database driver) can be tested instantly and reused anywhere.

```python
def to_rows(records, columns):
    """Pure core: works on plain lists and dicts, imports nothing."""
    return [[rec.get(c) for c in columns] for rec in records]

def to_frame(records, columns):
    """Adapter: pandas is only needed if you call this."""
    import pandas as pd   # lazy import
    return pd.DataFrame(to_rows(records, columns), columns=columns)

print(to_rows([{"a": 1, "b": 2}, {"a": 3}], ["a", "b"]))
print(to_frame([{"a": 1}], ["a"]).shape)
```

A top-level `import pandas` would make `import fmtkit` fail for anyone without pandas, and make it slow for everyone.

## Stable function signatures

Callers write `summarize(rows, "region")`. Anything that makes that call stop working is a breaking change. Habits that keep signatures stable:

- add new parameters **with defaults**, at the end
- make options **keyword-only** with a bare `*`, so nobody depends on their position
- never reorder or rename existing parameters

```python
def summarize(rows, key, *, top_n=None):
    counts = {}
    for r in rows:
        counts[r[key]] = counts.get(r[key], 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:top_n] if top_n else ranked

data = [{"r": "eu"}, {"r": "us"}, {"r": "eu"}, {"r": "apac"}]
print(summarize(data, "r"))
print(summarize(data, "r", top_n=1))
```

Keyword-only means callers must write `top_n=1`; they cannot pass a bare `1`, which would cement the argument order forever.

## What belongs in a shared library

Put code there when it is **stable, generic, and used by two or more projects**: date parsing rules, a warehouse connection helper, a retry decorator, validation of your company's ID formats. Keep out: code that encodes one project's business logic, anything that changes weekly, and "utils" grab bags. A library with a clear single purpose and a small API is one people trust.

A rule of thumb: copy once, copy twice, extract the third time. Extracting too early freezes a design you don't understand yet.

## Common mistakes

- No `__all__` and no underscore discipline, so every helper becomes public by accident.
- A circular import because `core.py` imports from `__init__.py`, which imports from `core.py`: `ImportError: cannot import name 'x' from partially initialized module`. Keep implementations independent of the package `__init__`.
- Importing a heavy dependency at module top level.
- Adding a required positional parameter to an existing function.

## What to take away

1. Anything importable without an underscore is a promise; keep the public surface small.
2. Re-export public names from `__init__.py` and list them in `__all__`.
3. Keep dependencies minimal and import optional ones lazily.
4. Evolve signatures with defaulted, keyword-only additions.
5. Extract to a library only code that is generic, stable and shared.
