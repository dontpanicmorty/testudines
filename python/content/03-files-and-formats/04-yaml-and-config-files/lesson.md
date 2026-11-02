+++
id = "files-and-formats.yaml-and-config-files"
title = "YAML and config files"
minutes = 25
+++

# YAML and config files

`dbt_project.yml`, `profiles.yml`, `schema.yml`, CI pipelines: you have lived in YAML for years. In Python, `yaml.safe_load` turns it into the same dicts and lists you got from JSON. This lesson is about the production habit around it: **config in files, secrets in the environment, defaults in code**.

> **SQL bridge.** A dbt `profiles.yml` reads `password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"`. The file describes *where* to look; the secret itself never lives in the repo. Same principle here.

## Loading YAML

```python
import yaml

text = """
pipeline:
  name: daily_orders
  retries: 3
  enabled: true
  tags: [core, finance]
  sources:
    - name: orders
      path: raw/orders.csv
    - name: customers
      path: raw/customers.csv
"""
cfg = yaml.safe_load(text)
print(cfg["pipeline"]["retries"], type(cfg["pipeline"]["retries"]))
print(cfg["pipeline"]["tags"])
print([s["name"] for s in cfg["pipeline"]["sources"]])
```

Always `safe_load`, never `yaml.load`. Plain `load` can construct arbitrary Python objects from a file, which is a code-execution risk.

YAML does the typing for you (`3` is an int, `true` a bool), which also bites:

> **Predict first.** What are the types of these values?

```python
import yaml

doc = yaml.safe_load("""
a: no
b: 1.10
c: 2025-01-31
d: "007"
e: null
f:
""")
for k, v in doc.items():
    print(k, repr(v), type(v).__name__)
```

`no` becomes `False`, `2025-01-31` becomes a `date`, an empty value becomes `None`. Quote anything that must stay text (`"007"`, `"no"`, version strings like `"1.10"`).

## Config layering

Production code rarely reads one file. It stacks layers, later ones winning:

1. defaults in code
2. a config file (per project or environment)
3. environment variables
4. command-line flags

Layering needs a **deep merge**: a plain `dict.update` replaces whole nested sections.

```python
def deep_merge(base, override):
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

defaults = {"db": {"host": "localhost", "port": 5432}, "retries": 3}
prod = {"db": {"host": "warehouse.internal"}}
print(deep_merge(defaults, prod))
print({**defaults, **prod})      # shallow: the port is lost
```

## Environment variables and secrets

```python
import os

os.environ["APP_RETRIES"] = "5"        # demo only; normally set by the shell or the platform

retries = int(os.environ.get("APP_RETRIES", "3"))   # env values are always str
token = os.environ.get("APP_TOKEN")                  # None if unset
print(retries, token)
```

Environment values are strings, so convert. For required secrets, fail early with a clear message instead of failing later with a confusing one:

```python
import os

def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

try:
    require_env("DOJO_SURELY_NOT_SET")
except RuntimeError as e:
    print(e)
```

Rules that keep you employed:

- **Never** hardcode a password, token or key, and never commit one, even in a "temporary" test.
- A config file may name the variable (`token_env: APP_TOKEN`) but not hold the value.
- Never print a whole config that may contain secrets. Log keys, mask values.

```python
def redact(cfg, secret_keys=("password", "token", "key", "secret")):
    out = {}
    for k, v in cfg.items():
        if isinstance(v, dict):
            out[k] = redact(v, secret_keys)
        elif any(s in k.lower() for s in secret_keys):
            out[k] = "***"
        else:
            out[k] = v
    return out

print(redact({"db": {"host": "h", "password": "p"}, "api_token": "t"}))
```

## Validate the result

A config typo should stop the run at startup, not three hours in. Check required keys and types once, right after loading.

```python
def validate(cfg):
    problems = []
    if not isinstance(cfg.get("retries"), int):
        problems.append("retries must be an int")
    if not cfg.get("sources"):
        problems.append("sources must be a non-empty list")
    return problems

print(validate({"retries": "3", "sources": []}))
```

Later in this stage you will turn this into proper exceptions and, in Stage 3, into pydantic models.

## Common mistakes

- `yaml.load(text)`: `TypeError: load() missing 1 required positional argument: 'Loader'`. The fix is `safe_load`, not passing a loader.
- Tabs in YAML: `found character '\t' that cannot start any token`. Use spaces.
- `ScannerError`/`ParserError` from bad indentation; the message includes line and column.
- Comparing `os.environ["DEBUG"] == True`. It is the string `"true"` or `"1"`, never a bool.

## What to take away

1. `yaml.safe_load` only; quote strings that look like other types.
2. Layer config: defaults, file, environment, flags, with a deep merge.
3. Environment values are strings; convert and fail early when required ones are missing.
4. Secrets come from the environment; never hardcode, commit or print them.
5. Validate config right after loading.
