+++
id = "testing-with-pytest.mocking-and-boundaries"
title = "Mocking and test boundaries"
minutes = 30
+++

# Mocking and test boundaries

Your dbt dev target points at a dev schema, never at prod. A unit test is stricter: it shouldn't touch *any* warehouse, clock, file system or API. Tests that do are slow, flaky (the API is down at 3am) and can do damage. The skill of this lesson is making code testable **without** touching the outside world.

> **SQL bridge.** `{{ target.schema }}` makes a model run against whichever schema you hand it. The Python equivalent is **dependency injection**: pass the thing that talks to the outside world *in*, so tests can pass a stand-in.

## Boundaries and the pure core

Most pipeline code is two kinds of logic mixed together: decisions (is this row late? which page is next?) and I/O (read the clock, call the API). Keep decisions in plain functions that take values and return values. Push I/O to thin edges. The core becomes trivially testable; the edges get a handful of tests with stand-ins.

## Dependency injection: pass the clock in

Naive version, which cannot be tested without waiting for real time to pass:

```python
# no-run
from datetime import datetime, timezone

def is_stale(loaded_at):
    return (datetime.now(timezone.utc) - loaded_at).total_seconds() > 3600
```

Idiomatic version, taking the "now" as a parameter with a real default:

```python
from datetime import datetime, timedelta, timezone

def is_stale(loaded_at, now=None):
    now = now or datetime.now(timezone.utc)
    return (now - loaded_at).total_seconds() > 3600

fixed_now = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
print(is_stale(fixed_now - timedelta(minutes=30), now=fixed_now))
print(is_stale(fixed_now - timedelta(hours=2), now=fixed_now))
```

No patching, no sleeping, and the test says exactly what time it is.

## Fakes: small working stand-ins

A **fake** is a simple real object with canned behaviour. It's often the best tool for an API client:

```python
class FakeClient:
    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def get_page(self, n):
        self.calls.append(n)
        return self.pages[n]          # unknown page -> KeyError, like a strict server

def count_users(client):
    total, page = 0, 1
    while page is not None:
        data = client.get_page(page)
        total += len(data["users"])
        page = data["next_page"]
    return total

fake = FakeClient({1: {"users": ["a", "b"], "next_page": 2},
                   2: {"users": ["c"], "next_page": None}})
print(count_users(fake), fake.calls)
```

For HTTP specifically, `httpx` ships a transport that answers requests from a function, so you can test the real client code without a network:

```python
import httpx

def handler(request):
    return httpx.Response(200, json={"users": ["a", "b"]})

client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.invalid")
print(client.get("/users").json())
```

## Mocks: record and verify interactions

`unittest.mock.Mock` accepts any call and remembers it. Use it when the *interaction* is what matters ("was the alert sent once?").

```python
from unittest.mock import Mock

send = Mock(return_value="sent")
print(send("ops@example.com", "load failed"))
send.assert_called_once_with("ops@example.com", "load failed")

flaky = Mock(side_effect=[ConnectionError("down"), {"ok": True}])
try:
    flaky()
except ConnectionError as exc:
    print("first call:", exc)
print("second call:", flaky())
print(flaky.call_count)
```

`side_effect` with a list returns or raises items one by one, which is perfect for testing retry logic.

**Fake or mock?** A fake has behaviour (it computes answers), so tests assert on *results*. A mock has none (you script answers) and tests assert on *calls*. Prefer fakes and results; reach for mocks to check a side effect that has no visible result.

## patch and monkeypatch: replacing things in place

When you can't inject (code you don't own, or a global like an environment variable), temporarily replace the thing. The golden rule: **patch the name where it is looked up**, not where it's defined.

> **Predict first.** `from os.path import exists` copies the function into your module's namespace. If you patch `os.path.exists`, does your module's `exists` change?

```python
from os.path import exists
from unittest.mock import patch

def has_marker():
    return exists("/definitely/not/here")

with patch("os.path.exists", return_value=True):
    print("patched the original:", has_marker())

with patch(f"{__name__}.exists", return_value=True):
    print("patched where it is used:", has_marker())
print("restored:", has_marker())
```

No: your module holds its own reference, so you must patch `<your_module>.exists`. pytest's `monkeypatch` fixture does the same job with automatic undo and is the everyday choice in test files:

```python
# no-run
def test_reads_warehouse_from_env(monkeypatch):
    monkeypatch.setenv("DOJO_WAREHOUSE", "wh_test")
    monkeypatch.delenv("DOJO_SCHEMA", raising=False)   # raising=False: fine if absent
    monkeypatch.setattr("mylib.settings.time.sleep", lambda s: None)
    assert load_settings()["warehouse"] == "wh_test"
```

## Files, time and network without touching them

- **Files**: don't mock `open`; write real files into `tmp_path`.
- **Time**: inject a clock, or `monkeypatch.setattr` the sleep function so retries don't wait.
- **Network**: inject a fake client, or use `httpx.MockTransport`.
- **Environment**: `monkeypatch.setenv` / `delenv`.
- **Warehouse**: pass a connection object in; test with an in-memory `sqlite3` or DuckDB database.

## Common mistakes

- Patching the wrong name: the test passes but real I/O still happens. Patch where it's used.
- Mocking the function under test; you then test your mock.
- Over-mocking: tests assert on every internal call and break on any refactor. Assert on outcomes.
- A `Mock()` silently accepts typos: `m.assert_called_once_wiht(...)` on old versions just creates an attribute. Modern mock raises `AttributeError: 'assert_called_once_wiht' is not a valid assertion`. Use `autospec=True` / `create_autospec` to make mocks match the real signature.
- Forgetting that `monkeypatch.delenv("X")` raises `KeyError` if `X` isn't set. Use `raising=False`.

## What to take away

1. Separate decisions from I/O, and test decisions as pure functions.
2. Inject dependencies (clock, client, connection) with real defaults.
3. Fakes give behaviour and are asserted on results; mocks record calls.
4. Patch where a name is looked up. Prefer `monkeypatch` in tests.
5. Use `tmp_path` for files, `MockTransport` for HTTP, `setenv` for config.
