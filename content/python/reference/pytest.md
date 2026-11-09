# pytest cheat sheet

## Running

```bash
# no-run
python -m pytest                    # everything under the current folder
python -m pytest -q                 # quiet
python -m pytest tests/test_x.py::test_name   # one test
python -m pytest -k "amount and not slow"     # by name expression
python -m pytest -m "not slow"      # by marker
python -m pytest -x                 # stop at first failure
python -m pytest --lf               # re-run last failures
python -m pytest -vv                # full diffs
```

Discovery: files `test_*.py` or `*_test.py`, functions `test_*`, classes `Test*` (no `__init__`).

## Assertions

```python
assert result == expected
assert 0.1 + 0.2 == pytest.approx(0.3)
assert "error" in message
with pytest.raises(ValueError, match="empty"):
    parse("")
with pytest.warns(DeprecationWarning):
    old_function()
```

## Fixtures

```python
@pytest.fixture
def rows():
    return [{"id": 1}, {"id": 2}]       # fresh per test

@pytest.fixture
def conn():
    c = open_test_db()
    yield c                              # test runs here
    c.close()                            # teardown

def test_it(rows, conn): ...
```

| Built-in | Gives you |
|---|---|
| `tmp_path` | empty `pathlib.Path` folder per test |
| `monkeypatch` | `setenv`, `delenv(raising=False)`, `setattr`, `chdir`, auto-undone |
| `capsys` | captured stdout/stderr: `capsys.readouterr().out` |
| `caplog` | captured log records |

Shared fixtures go in `conftest.py`. Use `scope="module"` only for read-only data.

## Parametrize

```python
@pytest.mark.parametrize(
    "raw, expected",
    [
        ("  Ada ", "ada"),
        pytest.param("", "", id="blank"),
    ],
)
def test_clean(raw, expected):
    assert clean(raw) == expected
```

## Markers

```python
@pytest.mark.skip(reason="...")
@pytest.mark.skipif(sys.platform == "win32", reason="posix only")
@pytest.mark.xfail(reason="ticket 123", strict=True)
@pytest.mark.slow          # custom: register under [tool.pytest.ini_options] markers
```

## Test doubles

```python
from unittest.mock import Mock, patch, create_autospec

m = Mock(return_value=42)
m.assert_called_once_with("a")
flaky = Mock(side_effect=[ConnectionError("down"), "ok"])

with patch("mymodule.requests_get", return_value=fake):   # patch where it is USED
    ...
```

| Need | Use |
|---|---|
| Time | inject `now=` callable, or `monkeypatch.setattr` |
| Files | `tmp_path` |
| HTTP | fake client class, or `httpx.MockTransport(handler)` |
| Environment | `monkeypatch.setenv` |
| Database | in-memory SQLite or DuckDB passed in |

## Testing data code

- Smallest input that shows each rule; compare exact output.
- Sort before comparing unordered results.
- DataFrames: `polars.testing.assert_frame_equal(actual, expected)`.
- Idempotency: `f(f(x)) == f(x)` over seeded random inputs.
- Do not mutate inputs: `before = copy.deepcopy(rows)` then assert unchanged.
- Golden files: compare whole text, review every regeneration.
- Schema drift: assert on missing, unexpected and type-changed columns.

## Config (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
markers = ["slow: takes more than a second"]
```
