+++
id = "snowflake-patterns-offline.auth-and-environments"
title = "Authentication and environments"
minutes = 25
+++

# Authentication and environments

You already think in roles, warehouses and databases every time you open a worksheet. A Python job has to say all of that **explicitly**, and say it differently in dev and prod, without a human to click the right dropdown. Mistakes here are expensive: a dev run pointed at prod, or a pipeline running as `ACCOUNTADMIN`.

> **Snowflake bridge.** `USE ROLE`, `USE WAREHOUSE`, `USE DATABASE` become keys in a parameter dict. dbt's `profiles.yml` targets (`dev`, `prod`) become a table of settings keyed by environment name.

## How a service proves who it is

| Method | Used by | Notes |
|---|---|---|
| Password | quick local experiments | weakest: shared secret; may be blocked by MFA policy |
| Key pair (JWT) | **services and pipelines** | private key stays with the job, public key registered on the user; rotate by swapping keys |
| SSO / browser (`externalbrowser`) | **humans** at a laptop | interactive: cannot run in CI or a scheduler |
| OAuth / workload identity | platform-managed jobs | tokens issued by your identity provider |

Rule: humans use SSO, machines use key pairs (or platform identity), and nobody pastes a password into code. The parameters differ, so your code picks them from what credentials are present:

```python
def auth_params(secrets: dict) -> dict:
    if "SF_PRIVATE_KEY_PATH" in secrets:
        return {"authenticator": "snowflake_jwt", "private_key_file": secrets["SF_PRIVATE_KEY_PATH"]}
    if "SF_PASSWORD" in secrets:
        return {"password": secrets["SF_PASSWORD"]}
    raise ValueError("no credentials found: set SF_PRIVATE_KEY_PATH or SF_PASSWORD")

print(auth_params({"SF_PRIVATE_KEY_PATH": "/run/secrets/key.p8"}))
print(auth_params({"SF_PASSWORD": "hunter2"}))
```

## Role, warehouse, database per environment

Keep one table of environments and look it up by name. Do not scatter `"PROD_WH"` strings around the code.

```python
ENVIRONMENTS = {
    "dev":  {"database": "ANALYTICS_DEV",  "warehouse": "DEV_WH",  "role": "LOADER_DEV"},
    "prod": {"database": "ANALYTICS",      "warehouse": "PROD_WH", "role": "LOADER"},
}

def environment(name: str) -> dict:
    try:
        return dict(ENVIRONMENTS[name])        # a COPY: callers may mutate it
    except KeyError:
        raise ValueError(f"unknown environment {name!r}; choose from {sorted(ENVIRONMENTS)}") from None

p = environment("dev")
p["schema"] = "SCRATCH"
print(p)
print(ENVIRONMENTS["dev"])        # untouched
```

> **Predict first.** If `environment` returned `ENVIRONMENTS[name]` directly and a caller added `"schema"`, what would the next caller see?

The mutated shared dict. Return copies of shared config.

## Least privilege

A job's role should be able to do **only** what the job does: `USAGE` on one warehouse, `INSERT`/`MERGE` on its target schema, `SELECT` on its sources. Concretely in code:

- One role per job family (loader, transformer, reporter), never `ACCOUNTADMIN` or `SECURITYADMIN` for automation.
- Refuse dangerous roles in code, as a seatbelt:

```python
FORBIDDEN_ROLES = {"ACCOUNTADMIN", "SECURITYADMIN"}

def check_role(role: str) -> str:
    if role.upper() in FORBIDDEN_ROLES:
        raise ValueError(f"role {role} is not allowed for automated jobs")
    return role

print(check_role("LOADER"))
try:
    check_role("accountadmin")
except ValueError as e:
    print("blocked:", e)
```

- Make production opt-in: require an explicit flag (or an environment variable only the scheduler sets), so a developer's `python job.py` hits dev by default.

## Query tags

`QUERY_TAG` is a session parameter that stamps every statement in the session. Later, `QUERY_HISTORY` can be filtered by tag to answer "which job caused this spend / this slow query?". Make the tag structured so it is searchable:

```python
import json

def query_tag(job: str, env: str, run_id: str) -> str:
    return json.dumps({"job": job, "env": env, "run": run_id}, sort_keys=True, separators=(",", ":"))

tag = query_tag("load_orders", "prod", "2026-11-02T06:00")
print(tag)
params = {"session_parameters": {"QUERY_TAG": tag}}
print(params)
```

## Assemble the parameters, log them safely

The final dict is what you hand to `connect(**params)`. Before logging it for diagnostics, mask the secrets.

```python
SECRET_KEYS = {"password", "private_key", "token", "passcode"}

def describe(params: dict) -> str:
    items = []
    for key in sorted(params):
        value = "***" if key in SECRET_KEYS else params[key]
        items.append(f"{key}={value}")
    return ", ".join(items)

print(describe({"account": "org-acct", "user": "SVC", "password": "hunter2", "role": "LOADER"}))
```

Note that `private_key_file` is a *path*, which is safe to show, while `private_key` is the key material itself.

## Common mistakes

- A default environment of `prod` so a typo or a missing variable runs against production.
- Returning the shared environment dict and letting callers mutate it.
- Running jobs as `ACCOUNTADMIN` "because it works".
- Printing the connection parameters (or an exception that contains them) with the password in it.
- Hard-coding the account, role or warehouse in the function that runs queries rather than in one config table.
- Forgetting that SSO needs a browser: `authenticator="externalbrowser"` hangs in a scheduler.

## What to take away

1. Services use key pairs or platform identity; SSO is for people; passwords are a last resort.
2. Role, warehouse and database come from one per-environment table, returned as copies.
3. Default to dev; make prod an explicit, deliberate choice.
4. Least privilege: one narrow role per job, with automation barred from admin roles.
5. Tag sessions with structured query tags, and redact secrets whenever parameters are logged.
