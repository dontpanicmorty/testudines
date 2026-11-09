+++
id = "modules-and-projects.project-layout"
title = "Project layout and pyproject.toml"
minutes = 30
+++

# Project layout and pyproject.toml

A dbt repo has a predictable shape: `dbt_project.yml` at the root, `models/`, `macros/`, `tests/`. Anyone can open it and know where things live. A Python project deserves the same: a standard layout, one config file, and clear names for what gets installed.

> **SQL bridge.** `dbt_project.yml` → `pyproject.toml` (name, version, dependencies, tool settings). `models/` → your package folder. `dbt run` → a command your package installs (an **entry point**).

## The recommended shape

```text
my-pipeline/
├── pyproject.toml
├── README.md
├── src/
│   └── mylib/
│       ├── __init__.py
│       ├── cleaning.py
│       ├── rows.py
│       └── cli.py
└── tests/
    └── test_cleaning.py
```

This is called the **src layout**. Your code lives under `src/`, not at the project root. Why? If `mylib/` sat at the root, then running tests from the root would import it straight from the folder whether or not it was installed. The tests would pass even when the packaging was broken. With `src/`, the only way to import `mylib` is to install it (`pip install -e .`), so your tests exercise the same thing users get.

## Packages and `__init__.py`

A **package** is a folder of modules. The file `__init__.py` marks it and runs when the package is imported. It is where you decide the package's *public face*:

```python
# no-run
# mylib/__init__.py
from .cleaning import clean_name
from .rows import read_rows

__all__ = ["clean_name", "read_rows"]
__version__ = "0.1.0"
```

Now users write `from mylib import clean_name` without knowing which file defines it. Keep `__init__.py` small: re-exports and a version, not logic.

Let's build a tiny real package on disk and import it:

```python
import sys
import tempfile
from pathlib import Path

root = Path(tempfile.mkdtemp())
pkg = root / "mylib"
pkg.mkdir()
(pkg / "__init__.py").write_text(
    "from .cleaning import clean_name\n__all__ = ['clean_name']\n"
)
(pkg / "cleaning.py").write_text(
    "def clean_name(raw):\n    return raw.strip().title()\n"
)
sys.path.insert(0, str(root))

import mylib
print(mylib.clean_name("  ada LOVELACE "))
print(mylib.__name__, mylib.clean_name.__module__)
```

## Absolute versus relative imports

Inside a package you can refer to a sibling two ways.

```python
# no-run
# mylib/transform.py
from mylib.cleaning import clean_name   # absolute: full path from the package root
from .cleaning import clean_name        # relative: "the cleaning module next to me"
from . import cleaning                  # relative: the sibling module itself
from ..other import helper              # two dots: the parent package
```

Prefer **absolute** imports for clarity; use **relative** ones inside a package when you want it to be rename-proof. What you must *not* do is `from cleaning import clean_name`: it only works if the package's own folder happens to be on `sys.path` (for example when you run a file from inside it) and fails as soon as the package is imported properly: `ModuleNotFoundError: No module named 'cleaning'`.

## `pyproject.toml` anatomy

One file describes the project. It is TOML, which Python can read itself:

```python
import tomllib

text = """
[project]
name = "mylib"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["pandas>=2.0", "httpx>=0.27"]

[project.scripts]
ingest = "mylib.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
"""

data = tomllib.loads(text)
print(data["project"]["name"], data["project"]["version"])
print(data["project"]["dependencies"])
print(sorted(data))
```

Three kinds of tables:

- `[project]`: identity and dependencies. This is what installers read.
- `[build-system]`: which tool builds the package. You rarely touch it.
- `[tool.*]`: settings for other tools (ruff, pytest, mypy) kept in one file.

## Entry points

`[project.scripts]` maps a command name to `"module:function"`. After installing, typing `ingest` in the terminal runs `mylib.cli.main()`. This replaces "run `python path/to/script.py`" with a real command that works from any folder.

```python
# no-run
# mylib/cli.py
def main() -> int:
    print("ingesting...")
    return 0
```

Keep `main` thin: parse arguments, call library functions, return an exit code. The logic stays importable and testable.

## Common mistakes

- `ModuleNotFoundError: No module named 'mylib'` when running tests: the package isn't installed into the active environment. Install it in editable mode.
- A missing `__init__.py` in a subfolder: usually still imports (as a "namespace package") but tools behave oddly. Add the file.
- Top-level `utils.py` dumping ground. Group by purpose: `cleaning`, `rows`, `models`.
- Circular imports between sibling modules: share a lower-level module instead.

## What to take away

1. The `src/` layout forces you to test the installed package, not a stray folder.
2. A package is a folder; `__init__.py` defines its public face.
3. Inside a package use absolute imports or explicit relative imports, never bare sibling names.
4. `pyproject.toml` holds project metadata, dependencies and tool config in one file.
5. `[project.scripts]` turns `module:function` into an installable command.
