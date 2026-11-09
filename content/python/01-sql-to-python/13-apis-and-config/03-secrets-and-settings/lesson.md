+++
id = "apis-and-config.secrets-and-settings"
title = "Secrets and settings"
minutes = 28
+++

# Secrets and settings

In dbt you never hard-code a password into a model: it lives in `profiles.yml` or an environment variable (`env_var('SNOWFLAKE_PASSWORD')`), and the project reads it at run time. Python services follow the same rule, usually called **12-factor config**: *code is the same everywhere; configuration comes from the environment.*

> **dbt bridge.** `target.name`, `env_var(...)` and `profiles.yml` per environment → environment variables read into one **settings object** at startup.

## Environment variables

`os.environ` is a dict-like mapping of strings.

```python
import os

os.environ["APP_REGION"] = "eu-west"      # normally set by the shell or the platform
print(os.environ["APP_REGION"])
print(os.environ.get("APP_MISSING"))      # None
print(os.environ.get("APP_MISSING", "default"))
```

`os.environ["X"]` raises `KeyError` when absent, `.get("X")` returns `None`. Everything is a **string**: `"10"` is not 10 and `"false"` is truthy.

> **Predict first.** What does `bool("false")` return?

```python
print(bool("false"), bool(""))
print(int("10") + 1)
```

`True`. Any non-empty string is truthy, so you must parse booleans yourself.

## Make configuration testable: pass the mapping in

Functions that read `os.environ` directly are hard to test. Accept a mapping argument that defaults to the real environment:

```python
import os
from collections.abc import Mapping

def parse_bool(text: str) -> bool:
    value = text.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off", ""}:
        return False
    raise ValueError(f"not a boolean: {text!r}")

def get_timeout(env: Mapping[str, str] = os.environ) -> float:
    return float(env.get("APP_TIMEOUT_S", "10"))

print(get_timeout({"APP_TIMEOUT_S": "2.5"}))
print(get_timeout({}))
print(parse_bool("Yes"), parse_bool("off"))
```

A plain `dict` works as a fake environment. No monkeypatching needed.

## A settings object, validated once

Instead of calling `os.environ.get` all over the code, read everything at **startup** into one typed, validated object and pass it around. Fail fast: a missing setting should stop the program before it does any work.

```python
from dataclasses import dataclass
from collections.abc import Mapping

class ConfigError(Exception):
    pass

@dataclass(frozen=True)
class Settings:
    api_url: str
    timeout_s: float = 10.0
    debug: bool = False

def load(env: Mapping[str, str]) -> Settings:
    if "APP_API_URL" not in env:
        raise ConfigError("missing required setting APP_API_URL")
    return Settings(
        api_url=env["APP_API_URL"],
        timeout_s=float(env.get("APP_TIMEOUT_S", "10")),
        debug=env.get("APP_DEBUG", "0") == "1",
    )

print(load({"APP_API_URL": "https://api.example.test", "APP_DEBUG": "1"}))
```

## The same thing with pydantic

pydantic does conversion (`"10"` to `10.0`, `"true"` to `True`) and reports every problem at once. Its `SecretStr` type hides a value when the object is printed or logged.

```python
from pydantic import BaseModel, SecretStr, ValidationError

class Settings(BaseModel, frozen=True):
    api_url: str
    api_token: SecretStr
    timeout_s: float = 10.0
    debug: bool = False

s = Settings(api_url="https://api.example.test", api_token="s3cret-token", timeout_s="2.5", debug="true")
print(s)
print(s.timeout_s, s.debug)
print(s.api_token.get_secret_value())   # only when you truly need it

try:
    Settings(timeout_s="soon")
except ValidationError as exc:
    print([e["loc"][0] for e in exc.errors()])
```

`get_secret_value()` is deliberately awkward: use it at the last moment (building an auth header), never when logging.

## Secrets: what never goes in git

Never commit passwords, tokens, private keys or connection strings with credentials. History is forever: a secret deleted in a later commit is still in the repository and must be treated as leaked and **rotated**. Habits that prevent it:

- Keep a local `.env` file (one `KEY=value` per line) and list it in `.gitignore`.
- Commit a `.env.example` with fake values and comments so teammates know what to set.
- In deployed environments the platform injects variables from a secret manager; no file.

## Reading .env without extra libraries

```python
def parse_dotenv(text: str) -> dict[str, str]:
    values = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"line {number}: expected KEY=VALUE")
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        values[key.strip()] = value
    return values

sample = """
# local settings
APP_API_URL=https://api.example.test
APP_API_TOKEN="abc def"
"""
print(parse_dotenv(sample))
```

`partition("=")` splits on the **first** equals sign only, so values like base64 text containing `=` survive. Real environment variables should win over the file: `{**dotenv, **os.environ}`.

## Redacting secrets in logs

Logs are copied into tickets, chat and dashboards. Mask secret-looking keys before anything is printed.

```python
SENSITIVE = ("token", "secret", "password", "key")

def redact(data: dict) -> dict:
    return {
        k: "***" if any(w in k.lower() for w in SENSITIVE) else v
        for k, v in data.items()
    }

print(redact({"user": "svc_loader", "password": "hunter2", "API_TOKEN": "abc", "region": "eu"}))
```

Redact by **key name** and, for nested payloads, recurse. Never log full request headers: `Authorization` carries the token.

## Common mistakes

- `os.environ["APP_PORT"] + 1` raises `TypeError: can only concatenate str (not "int") to str`. Convert first.
- `if os.environ.get("DEBUG"):` is true for `"0"` and `"false"`. Parse booleans.
- `KeyError: 'APP_API_URL'` deep inside a job at 3 a.m. Validate at startup and name the missing variables.
- Committing `.env`. If it happens, rotate the secret; deleting the file is not enough.
- Printing the settings object, or `repr(headers)`, at debug level.
- Default values for secrets (`token = os.environ.get("TOKEN", "dev-token")`) that quietly work in production.

## What to take away

1. Code is constant; configuration comes from environment variables.
2. Environment values are strings: parse and validate them once, at startup.
3. Take a mapping argument so tests pass a dict instead of mutating `os.environ`.
4. Fail fast and list every missing setting.
5. Secrets stay out of git, out of defaults, and out of logs (`SecretStr`, redaction).
