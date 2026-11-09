# Project layout cheat sheet

## src layout

```text
my-pipeline/
├── pyproject.toml
├── README.md
├── uv.lock                 # lock file (commit it)
├── .python-version
├── src/
│   └── mylib/
│       ├── __init__.py     # public face: re-exports, __version__
│       ├── cleaning.py
│       ├── rows.py
│       └── cli.py          # main() for the entry point
└── tests/
    ├── conftest.py
    └── test_cleaning.py
```

Never commit `.venv/`. Install your own package in editable mode so tests import the installed code.

## pyproject.toml

```toml
[project]
name = "mylib"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["pandas>=2.0", "httpx>=0.27"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[project.scripts]
ingest = "mylib.cli:main"       # command = "package.module:function"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
strict = true
```

Read it from Python with `tomllib.loads(text)`.

## Imports

| Style | Example | Use |
|---|---|---|
| Absolute | `from mylib.cleaning import clean_name` | default choice |
| Relative | `from .cleaning import clean_name` | siblings inside a package |
| Parent | `from ..shared import helper` | one level up |
| Bare sibling | `from cleaning import clean_name` | never inside a package |

- First import runs the file and caches it in `sys.modules`.
- Python searches `sys.path` in order; your own folder is first, so don't name files `json.py` or `csv.py`.
- Guard scripts: `if __name__ == "__main__": main()`.
- Circular imports: move shared code to a third module, or inject the dependency.

## Environments

```bash
# no-run
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
python -m pytest
```

```python
import sys
sys.prefix != sys.base_prefix    # True inside a venv
```

| File | Purpose |
|---|---|
| requirements / `dependencies` | what you need (loose ranges) |
| lock file | exact versions installed; deploy from this |

## Quality gates (CI)

```bash
# no-run
python -m ruff check .
python -m ruff format --check .
python -m mypy src
python -m pytest
```
