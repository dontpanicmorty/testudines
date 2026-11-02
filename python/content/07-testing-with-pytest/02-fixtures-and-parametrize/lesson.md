+++
id = "testing-with-pytest.fixtures-and-parametrize"
title = "Fixtures, parametrize and markers"
minutes = 30
+++

# Fixtures, parametrize and markers

dbt gives you two ways to test without copy-pasting: **seeds** (small known input data that every test can use) and generic tests that you point at many columns. pytest has the same two ideas, called **fixtures** and **parametrize**.

> **SQL bridge.** A fixture ≈ a seed or a CTE of known rows that tests share. `parametrize` ≈ a `VALUES (...)` table of cases: one test body, many rows of input and expected output.

## Fixtures: shared setup with a name

Write a function decorated with `@pytest.fixture`. Any test that lists the fixture's name as an argument receives its return value. pytest builds a **fresh** one per test.

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def run_pytest(source, *flags):
    folder = Path(tempfile.mkdtemp())
    (folder / "test_demo.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--disable-warnings", *flags, "test_demo.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print("\n".join(r.stdout.splitlines()[:-1]))

run_pytest('''
import pytest

@pytest.fixture
def orders():
    return [{"id": 1, "total": 40}, {"id": 2, "total": 0}, {"id": 3, "total": 25}]

def test_counts_paid_orders(orders):
    assert len([o for o in orders if o["total"] > 0]) == 2

def test_each_test_gets_its_own_copy(orders):
    orders.append({"id": 4, "total": 1})
    assert len(orders) == 4

def test_so_this_still_sees_three(orders):
    assert len(orders) == 3
''')
```

Because each test gets a new list, the second test's `append` can't leak into the third. That isolation is the point. A fixture that returns a **module-level** object defeats it (see Common mistakes).

Fixtures can set up *and clean up* with `yield`. Everything after `yield` runs when the test finishes, pass or fail:

```python
# no-run
@pytest.fixture
def connection():
    conn = open_test_database()
    yield conn            # the test runs here
    conn.close()          # teardown
```

Fixtures shared by several test files live in a file called `conftest.py` in the tests folder. pytest loads it automatically; you never import it.

## tmp_path: a private folder per test

For code that reads and writes files, don't touch real paths. pytest provides a built-in fixture, `tmp_path`, a fresh empty `pathlib.Path` folder that is cleaned up automatically.

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def run_pytest(source, *flags):   # same helper as above
    folder = Path(tempfile.mkdtemp())
    (folder / "test_demo.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--disable-warnings", *flags, "test_demo.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print("\n".join(r.stdout.splitlines()[:-1]))

run_pytest('''
def load_names(path):
    return [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]

def test_load_names_skips_blank_lines(tmp_path):
    f = tmp_path / "names.txt"
    f.write_text("ada\\n\\n grace \\n")
    assert load_names(f) == ["ada", "grace"]
''')
```

Combine the ideas: a fixture can itself use `tmp_path` to write a small CSV, and every test in the file reuses it.

## parametrize: a table of cases

Here is the naive version of testing a cleaner:

```python
# no-run
def test_clean_1(): assert clean("  Ada ") == "ada"
def test_clean_2(): assert clean("ADA") == "ada"
def test_clean_3(): assert clean("") == ""
```

The idiomatic version is a table. Each row becomes its own test with its own pass/fail result:

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def run_pytest(source, *flags):   # same helper as above
    folder = Path(tempfile.mkdtemp())
    (folder / "test_demo.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--disable-warnings", *flags, "test_demo.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print("\n".join(r.stdout.splitlines()[:-1]))

run_pytest('''
import pytest

def clean(raw):
    return raw.strip().lower()

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("  Ada ", "ada"),
        ("ADA", "ada"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_clean(raw, expected):
    assert clean(raw) == expected
''', "--collect-only")
```

Four rows, four tests (`test_clean[  Ada -ada]`, ...). A failure names the exact row. Add `ids=[...]` or use `pytest.param(..., id="blank")` to make the labels readable. Data-cleaning functions are where this shines: when you discover a new dirty input in production, add one row to the table and you've both fixed and permanently guarded against it.

Parametrize can stack: two decorators multiply into every combination.

## Markers: labelling tests

A **marker** tags a test so you can select, skip or expect failure.

```python
# no-run
@pytest.mark.skip(reason="waiting on upstream fix")
def test_not_yet(): ...

@pytest.mark.xfail(reason="known bug, ticket 123", strict=True)
def test_known_bug(): ...

@pytest.mark.slow
def test_full_reload(): ...
```

- `skip`: don't run it.
- `xfail`: expected to fail. With `strict=True` it turns red if it unexpectedly passes, telling you to remove the marker.
- custom markers like `slow`: run only some tests with `python -m pytest -m "not slow"`. Register custom marker names in `pyproject.toml` under `[tool.pytest.ini_options] markers = [...]` so typos are caught.

## Common mistakes

- A fixture returning a module-level mutable (`SHARED = []`) so tests contaminate each other, causing order-dependent failures. Create the object *inside* the fixture.
- Forgetting the fixture argument: `NameError: name 'orders' is not defined`. The name must appear in the test's parameters.
- Names in `parametrize("raw, expected", ...)` that don't match the test's parameter names: `ValueError: ... uses no argument 'expected'`.
- Putting expensive setup in a fixture that every test repeats. Use `scope="module"` for read-only data. Don't use it for anything tests modify.
- Overusing fixtures for trivial values; a plain local variable is clearer.

## What to take away

1. A fixture is a named, reusable setup that tests request by argument; it's rebuilt per test by default.
2. Use `tmp_path` for any file work; never touch real paths.
3. `parametrize` turns one test body into a table of cases. Add a row for every new dirty input you meet.
4. `yield` fixtures get teardown for free; `conftest.py` shares fixtures across files.
5. Markers: `skip`, `xfail`, and your own labels such as `slow`.
