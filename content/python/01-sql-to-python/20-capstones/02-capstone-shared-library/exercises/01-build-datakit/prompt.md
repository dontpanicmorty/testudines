Implement `datakit`, a small library other people will `pip install`. The tests behave like a **consumer**: they only `import datakit` and use its public API, and a separate test file guards that API against accidental breakage.

## Public API (everything importable from `datakit`)

`__version__ = "1.0.0"` (not in `__all__`) and `__all__` containing exactly:
`ConfigError`, `ConnectionProtocol`, `DatabaseError`, `DatakitError`, `RowValidator`, `SqliteConnection`, `load_config`, `retry`.

**Errors** (`errors.py`, provided): `DatakitError` base; `ConfigError(errors: list[str])`; `DatabaseError`.

**`load_config(cls, source=None, prefix="")`**: `cls` is a dataclass. Field `max_rows` is read from key `PREFIX + "MAX_ROWS"` in `source` (default `os.environ`). Convert by annotation: `str`, `int`, `float`, `bool` (`1/true/yes/on` and `0/false/no/off`, case-insensitive, whitespace trimmed). Fields with defaults (or `default_factory`) may be missing; `X | None` fields without a default become `None`. Otherwise a missing key is the message `"DB_PATH: missing"`; an unparsable value is `"MAX_ROWS: cannot parse 'many' as int"`. **All** problems are reported together, in field order, in one `ConfigError` (`.errors`, and `str()` joins them with `"; "`). A non-dataclass raises `TypeError`. Do not mutate `source`.

**`retry(attempts=3, delay=0.0, backoff=2.0, exceptions=(Exception,), sleep=time.sleep)`**: a decorator factory. Retries only for the listed exceptions, sleeping `delay * backoff**n` before retry `n+1` (no sleep after the final attempt). After the last attempt the **original** exception is re-raised. Preserve the function's name and docstring. Invalid arguments (`attempts < 1`, `delay < 0`, `backoff < 1`) raise `ValueError` when `retry(...)` is called.

**`RowValidator(*, required=(), types=None, checks=None)`** (keyword-only). `errors(row)` returns messages in this order: all `required` problems (missing, `None` or blank string: `"field: required"`), then type problems (`"field: expected int"`; a `bool` is not an `int`), then check problems (`"field: failed check"`; a check that raises counts as failed; checks and type tests are skipped for absent fields, and checks are skipped when the type is already wrong). `split(rows)` returns `(valid_copies, [(invalid_copy, errors), ...])`.

**`ConnectionProtocol`**: a `runtime_checkable` `Protocol` with `query(sql, params=()) -> list[dict]`, `execute(sql, params=()) -> int` (rows affected) and `close()`.

**`SqliteConnection(path=":memory:")`** implements it, plus `executemany(sql, rows)` and a `transaction()` context manager (commit on success, rollback on any exception, nested use joins the outer transaction). Outside a transaction, `execute` autocommits. `sqlite3.Error` becomes `DatabaseError` with the original as `__cause__`. It works as a context manager that closes the connection.

All public callables need type hints and docstrings, and library code never prints.

## Rubric

- Behavior of each component, including every edge case above
- Consumer-style tests: a fake connection works anywhere a `ConnectionProtocol` is expected
- Public API stays exactly as specified (names, parameter names and defaults, keyword-only arguments, exception hierarchy)
- Typed, documented, side-effect-free library code
