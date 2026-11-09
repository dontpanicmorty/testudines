+++
id = "testing-with-pytest.first-tests"
title = "Your first tests"
minutes = 25
+++

# Your first tests

In dbt you write `not_null` and `unique` tests and a failing one tells you exactly which model broke. Python testing with **pytest** gives you the same safety net for functions: change a cleaning rule on Friday, and a red test tells you which behaviour you just broke before Monday's load does.

> **SQL bridge.** A dbt singular test is a query that returns the *bad* rows. A pytest test is a function that states a fact with `assert`. If the fact is false, the test fails.

## A test is a function with an assert

```python
def total_cents(prices):
    return sum(round(p * 100) for p in prices)

def test_total_cents_adds_prices():
    assert total_cents([1.10, 2.20]) == 330

def test_total_cents_of_nothing_is_zero():
    assert total_cents([]) == 0

test_total_cents_adds_prices()
test_total_cents_of_nothing_is_zero()
print("both facts hold")
```

`assert expr` does nothing when `expr` is truthy and raises `AssertionError` when it isn't. pytest's job is to find your test functions, call them, and report nicely. You don't call them yourself.

## Discovery rules

pytest looks for files named `test_*.py` (or `*_test.py`), and inside them for functions named `test_*`. Put tests in a `tests/` folder next to your package, as in the project-layout lesson. That's all the configuration you need.

```bash
# no-run
python -m pytest            # run everything found
python -m pytest -q         # quieter
python -m pytest tests/test_cleaning.py::test_strips_spaces   # one test
python -m pytest -k "amount"   # tests whose name contains "amount"
```

## Running pytest from an example

To see real pytest output here, this helper writes a test file to a temporary folder and runs it. You'll reuse the pattern in later lessons.

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def run_pytest(source):
    folder = Path(tempfile.mkdtemp())
    (folder / "test_demo.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short",
           "-p", "no:cacheprovider", "--disable-warnings", "test_demo.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print("\n".join(r.stdout.splitlines()[:-1]))   # drop the timing line

run_pytest('''
def total_cents(prices):
    return sum(round(p * 100) for p in prices)

def test_total_cents():
    assert total_cents([1.10, 2.20]) == 331

def test_empty():
    assert total_cents([]) == 0

def test_dict():
    assert {"a": 1, "b": 2} == {"a": 1, "b": 3}
''')
```

## Reading a failure

The output of that run (abridged), in the order you should read it:

```text
F.F                                                  [100%]
=================================== FAILURES ===================================
_______________________________ test_total_cents _______________________________
test_demo.py:6: in test_total_cents
    assert total_cents([1.10, 2.20]) == 331
E   assert 330 == 331
E    +  where 330 = total_cents([1.1, 2.2])
__________________________________ test_dict ___________________________________
test_demo.py:12: in test_dict
    assert {"a": 1, "b": 2} == {"a": 1, "b": 3}
E   AssertionError: assert {'a': 1, 'b': 2} == {'a': 1, 'b': 3}
E     Differing items:
E     {'b': 2} != {'b': 3}
```

1. The dots-and-letters line: `F.F` means fail, pass, fail, one character per test.
2. Each failing test gets a banner with its name.
3. The `E` lines are the story: what the left side actually was, what the right side was, and for dicts and lists exactly what differs.

Here the test itself was wrong (330 is correct), which is a reminder that a failing test means "code and expectation disagree". Decide who is right.

## Arrange, act, assert

Keep each test in three visible parts. It makes tests readable months later.

```python
def clean_email(raw):
    return raw.strip().lower()

def test_clean_email_lowercases_and_strips():
    # arrange
    raw = "  Ada@Example.COM "
    # act
    result = clean_email(raw)
    # assert
    assert result == "ada@example.com"

test_clean_email_lowercases_and_strips()
print("ok")
```

One behaviour per test, named after that behaviour: `test_blank_amount_becomes_none` beats `test_parse_3`. When it fails, the name alone tells you what broke.

## Floats and exceptions

Floats are approximate (you met this in Stage 1), so compare with `pytest.approx`. To assert that code *refuses* bad input, use `pytest.raises`:

```python
import pytest

def average(xs):
    if not xs:
        raise ValueError("average of empty list")
    return sum(xs) / len(xs)

def test_average_is_approximate():
    assert average([0.1, 0.2]) == pytest.approx(0.15)

def test_average_rejects_empty():
    with pytest.raises(ValueError, match="empty"):
        average([])

test_average_is_approximate()
test_average_rejects_empty()
print("ok")
```

## What to test in a pure function

A pure function (same inputs, same output, no side effects) is the easiest thing to test: no setup, no cleanup. For each one, cover:

- the typical case,
- each **boundary** (0, 1, the limit, one past the limit),
- the "nothing" cases (empty, `None`, blank),
- each documented error.

If a function has four `if` branches, you want at least four tests, one to reach each branch.

## Common mistakes

- Tests that can never fail: `assert result` (true for any non-empty value) or no assert at all. Ask of every test: *what bug would make this go red?*
- Asserting on the whole printed output when one field matters.
- `assert x == y` with floats and no `approx`.
- Naming the file `tests.py` or `check_cleaning.py`: pytest silently finds nothing and reports `no tests ran`.
- Tests that depend on each other's order or leftovers.

## What to take away

1. A test is a function named `test_*` in a file named `test_*.py`, using plain `assert`.
2. Read failures from the `E` lines: actual vs expected.
3. Arrange, act, assert, one behaviour per test.
4. Test the typical case, the boundaries, the empties and the errors.
5. Use `pytest.approx` for floats and `pytest.raises` for expected errors.
6. A good test is one you can imagine failing.
