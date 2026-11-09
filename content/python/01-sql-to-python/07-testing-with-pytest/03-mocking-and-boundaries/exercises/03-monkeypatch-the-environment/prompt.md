`settings.connection_settings()` reads warehouse settings from environment variables:

- `DOJO_WAREHOUSE`: **required**, non-blank (surrounding whitespace is ignored). Otherwise raise `ConfigError`.
- `DOJO_SCHEMA`: optional, default `"analytics"`.
- `DOJO_TIMEOUT`: optional integer seconds, default `30`. It must be positive; a non-integer or a value `<= 0` raises `ConfigError`.

It returns `{"warehouse": ..., "schema": ..., "timeout": <int>}`.

Write `my_tests.py` using the `monkeypatch` fixture so tests never depend on your real environment. It must pass on the real function and catch every hidden-bug variant.

```python
from settings import connection_settings, ConfigError
connection_settings()   # {'warehouse': 'wh_test', 'schema': 'analytics', 'timeout': 30}
```

Write at least 5 tests.
