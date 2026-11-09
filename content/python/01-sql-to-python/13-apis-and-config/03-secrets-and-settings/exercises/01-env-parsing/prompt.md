Environment variables are always strings. Write two helpers (the environment is passed in as a mapping so tests can use a dict):

- `parse_bool(text)`: case-insensitive, ignoring surrounding whitespace. `1/true/yes/on` give `True`; `0/false/no/off` and the empty string give `False`. Anything else raises `ValueError`.
- `get_int(env, name, default)`: returns `default` when `name` is absent; otherwise the int value. A value that is not an integer raises `ConfigError` whose message contains the variable name.

```python
parse_bool(" Yes ")                     # True
get_int({"APP_BATCH": "500"}, "APP_BATCH", 100)   # 500
get_int({}, "APP_BATCH", 100)                      # 100
get_int({"APP_BATCH": "lots"}, "APP_BATCH", 100)   # ConfigError mentioning APP_BATCH
```
