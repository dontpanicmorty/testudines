Write `build_config(defaults, file_cfg, env, prefix="APP_")`.

1. Start with `defaults`, deep-merge `file_cfg` over it (nested dicts merge, other values replace).
2. For every **top-level** key in the result, if `env` has `prefix + KEY.upper()`, override it, converting the string to the type of the current value: `int` -> `int(...)`, `bool` -> true when the text lowercased is in `{"1", "true", "yes"}`, anything else stays `str`.
3. Do not modify the inputs. `env` is a plain dict (tests pass one in; do not read `os.environ`).

```python
build_config({"retries": 3, "db": {"host": "h", "port": 1}},
             {"db": {"host": "prod"}},
             {"APP_RETRIES": "5"})
# {"retries": 5, "db": {"host": "prod", "port": 1}}
```
