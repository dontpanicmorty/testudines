# Snowflake from Python: patterns cheat sheet

## Lifecycle

| Step | Code | Notes |
|---|---|---|
| connect | `conn = connect(**params)` | once per job; role, warehouse, database set here |
| cursor | `cur = conn.cursor()` | cheap; one per statement |
| execute | `cur.execute(sql, params)` | returns the cursor |
| fetch | `fetchone()` / `fetchmany(n)` / `fetchall()` | tuples; `None` when exhausted |
| metadata | `cur.description`, `cur.rowcount` | `description` is `None` without a result set |
| close | `with conn: with conn.cursor() as cur:` | cleanup even on error |

```python
# no-run
with connect(**params) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM t WHERE region = %(r)s", {"r": "EU"})
        rows = cur.fetchall()
```

## Binding

| Style | Placeholder | Params |
|---|---|---|
| pyformat | `%(name)s` | dict |
| format | `%s` | tuple / list |
| qmark | `?` | tuple (needs the connector's paramstyle set) |

Values bind; identifiers (table, column names) do not: validate them with `^[A-Za-z_][A-Za-z0-9_$]*$`.

## Loading

| Need | Use |
|---|---|
| a few rows | `executemany` in batches, one transaction |
| thousands to billions | files, `PUT` to a stage, `COPY INTO` |
| DataFrame in memory | `write_pandas`-style: Parquet to temp stage, then `COPY INTO` |
| rerunnable / late data | load to a staging table, `MERGE` on the business key |

```python
from itertools import islice

def batched(items, size):
    it = iter(items)
    while chunk := list(islice(it, size)):
        yield chunk
```

Idempotent shape: `TEMP staging table -> COPY INTO staging -> dedupe -> MERGE INTO target`.

## Auth and environments

| Who | Method |
|---|---|
| service / pipeline | key pair (JWT) or platform identity |
| person | SSO (`externalbrowser`) |
| last resort | password |

- One config table per environment (database, warehouse, role); return **copies**.
- Default to dev; make prod an explicit opt-in.
- Least privilege: a narrow role per job; never `ACCOUNTADMIN` / `SECURITYADMIN` for automation.
- Session `QUERY_TAG` as compact JSON: `{"env":"dev","job":"load_orders","run":"..."}`.
- Redact `password`, `private_key`, `token`, `passcode` before logging parameters.

## Testing

| Layer | Tool | Asserts |
|---|---|---|
| contract | hand-written fake connection | SQL text, bound params, commit/rollback, close |
| generated SQL | whitespace-normalised equality | full statement, not fragments |
| SQL logic | in-memory DuckDB | dedupe, windows, aggregates (`QUALIFY` works in both engines) |
| integration | dev warehouse (outside this course) | engine-specific behaviour |

```python
def job(connect, day):          # inject a factory, never build the connection inside
    conn = connect()
    try:
        ...
    finally:
        conn.close()
```

DuckDB differences to remember: `?` / `$name` placeholders, no stages or `COPY INTO @stage`, some semi-structured functions differ.
