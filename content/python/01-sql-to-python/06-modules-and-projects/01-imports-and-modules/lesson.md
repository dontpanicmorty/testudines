+++
id = "modules-and-projects.imports-and-modules"
title = "Imports and modules"
minutes = 25
+++

# Imports and modules

A dbt project is a folder of files that reference each other through `ref()`. Python works the same way: every `.py` file is a **module**, and `import` is how one file uses another. Understanding what `import` actually *does* explains a whole family of confusing errors.

> **SQL bridge.** `schema.table` namespacing → `module.name`. `ref('orders')` → `import orders`. A model that depends on itself through another model is a cycle in the DAG; Python has the same problem, and no tool to resolve it for you.

## The import forms

```python
import math                    # bind the module; use math.sqrt
import math as m               # same module, shorter label
from math import sqrt, pi      # bind specific names directly
from math import sqrt as root  # bind one name under another label

print(math.sqrt(16), m.sqrt(16), sqrt(16), root(16))
print(round(pi, 3))
```

Which one? Prefer `import module` or `from module import name` with explicit names. Avoid `from module import *`: it dumps unknown names into your file, so readers (and linters) cannot tell where `clean` came from.

A module is just an object. Its names are attributes:

```python
import math
print(type(math))
print(math.__name__)
print("sqrt" in dir(math))
```

## What import really does

The first time you import a module, Python (1) finds the file, (2) **runs it top to bottom**, (3) stores the resulting module object in the cache `sys.modules`. Every later import of the same name just fetches the cached object. Nothing runs twice.

> **Predict first.** A module prints `"loading greeter"` at its top level. You import it twice. How many times do you see the message?

```python
import sys
import tempfile
import pathlib

folder = pathlib.Path(tempfile.mkdtemp())
(folder / "greeter.py").write_text('print("loading greeter")\nGREETING = "hello"\n')
sys.path.insert(0, str(folder))

import greeter
import greeter

print(greeter.GREETING)
print("greeter" in sys.modules)
```

Once. Top-level code runs at first import only. That is why modules should mostly contain definitions (functions, classes, constants), not actions.

## Where does Python look? `sys.path`

When you write `import greeter`, Python walks the list `sys.path` in order and takes the first match. The list holds the script's own directory first, then the standard library, then `site-packages` (where installed packages live).

```python
import sys
print(type(sys.path), len(sys.path) > 2)
print(any(p.endswith("site-packages") for p in sys.path))
```

Two consequences. First, a file of yours named `json.py` or `random.py` *shadows* the standard module of that name, because your folder is searched first. Second, "works on my machine" bugs are often a `sys.path` difference.

## `if __name__ == "__main__":`

Every module has a `__name__`. When you *run* a file it is `"__main__"`; when it is *imported* it is the module's name.

```python
print(__name__)
```

That lets one file be both a library and a script:

```python
def total(rows):
    return sum(rows)


def main():
    print(total([10, 20, 30]))


if __name__ == "__main__":
    main()
```

Without the guard, importing the file would run `main()` as a side effect: a test import that sends emails or loads a warehouse table. Always guard script behaviour.

## Circular imports

`a.py` imports `b.py` at the top, and `b.py` imports `a.py` at the top. Python starts running `a`, hits the import of `b`, starts running `b`, which asks for names from `a` that don't exist yet, because `a` only got as far as its first line.

```python
# no-run
# customers.py
from orders import orders_for          # line 1: pauses here, runs orders.py

# orders.py
from customers import get_customer     # asks a half-built module for a name
# ImportError: cannot import name 'get_customer' from partially initialized
# module 'customers' (most likely due to a circular import)
```

Ways out, best first:

1. **Move the shared piece into a third module** that both import. The cycle was a design smell: two modules that need each other are really one idea plus a shared dependency.
2. **Pass the dependency in** as an argument instead of importing it.
3. **Import inside the function** that needs it. It works, because by call time both modules are fully loaded, but it hides the dependency. Use it as a last resort.

## Common mistakes

- Naming your file `test.py`, `types.py` or `csv.py` and breaking imports: `AttributeError: module 'csv' has no attribute 'reader'`. Rename it.
- Editing a module and re-importing in the same running session: the cached version is reused. Restart, or `importlib.reload`.
- `ModuleNotFoundError: No module named 'helpers'`: the folder holding `helpers.py` is not on `sys.path`. Check where you are running from.
- Putting real work at module top level, then wondering why importing is slow or has side effects.

## What to take away

1. A module is a file; `import` runs it once and caches it in `sys.modules`.
2. Python searches `sys.path` in order; the first match wins.
3. `from x import *` hides where names come from. Be explicit.
4. Guard script behaviour with `if __name__ == "__main__":`.
5. A circular import means the design needs a third module (or injected dependency).
