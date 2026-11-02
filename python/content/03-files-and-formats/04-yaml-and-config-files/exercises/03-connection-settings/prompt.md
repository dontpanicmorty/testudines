A warehouse config looks like this (parsed from YAML):

```python
cfg = {"account": "acme", "user": "svc_etl", "password_env": "WH_PASSWORD", "warehouse": "LOAD_WH"}
```

Write two functions (no real connection is ever made):

- `connection_params(cfg, env)` returns `{"account", "user", "warehouse", "password"}` where `password` is looked up in `env` (a dict) under the name given by `cfg["password_env"]`. If that variable is missing or empty, raise `RuntimeError` whose message contains the variable **name**.
- `describe(cfg)` returns a one-line string safe to log, such as `"acme/svc_etl on LOAD_WH (password from WH_PASSWORD)"`. It must never contain a password value.

```python
connection_params(cfg, {"WH_PASSWORD": "s3cret"})["password"]   # "s3cret"
describe(cfg)   # "acme/svc_etl on LOAD_WH (password from WH_PASSWORD)"
```
