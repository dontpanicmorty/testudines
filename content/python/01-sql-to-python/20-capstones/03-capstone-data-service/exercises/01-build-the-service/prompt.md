Build the service described in the lesson brief in the package `revenue_api/`. It serves a DuckDB database that already contains two tables:

```sql
daily_revenue(day DATE, region VARCHAR, orders INTEGER, revenue DOUBLE)
customers(customer_id INTEGER, first_name VARCHAR, last_name VARCHAR, email VARCHAR,
          region VARCHAR, plan VARCHAR, signup_date DATE)
```

Tests drive the app only through `TestClient` and replace `get_settings` and `get_today` with `app.dependency_overrides`. No server is ever started.

## Files

`settings.py` (`Settings`, `get_settings`, `get_today`), `db.py` (`connect`, `get_conn`, `fetch_all`), `models.py`, `errors.py` (`install_error_handlers`), `app.py` (`create_app()` and the routes). Starter files contain the intended shapes and TODOs.

## Endpoints

| Method and path | Behavior |
|---|---|
| `GET /health` | `200 {"status": "ok", "database": "up"}` after `select 1` on a fresh connection; `503 {"status": "degraded", "database": "down"}` if the database cannot be opened. Needs no tables. |
| `GET /revenue/daily` | Query: `start`, `end` (dates, inclusive), `region`, `page`, `page_size`. Returns `{"items": [{"day","region","orders","revenue"}], "page","page_size","total","has_next"}` ordered by `day, region`; `revenue` rounded to 2 places; `total` counts all matching rows. `start > end` is `422` with `"query.start"` in `fields`. An unknown region is an empty page, not an error. |
| `GET /revenue/daily/{day}` | `{"day", "orders", "revenue", "regions": [{"region","orders","revenue"}...]}` (regions ordered by name, totals are sums). `404` if the day has no rows, `422` for a bad date. |
| `GET /customers` | Filters `region`, `plan`; same pagination; ordered by `customer_id`. Items are `Customer` (**never include `email`**). |
| `GET /customers/{customer_id}` | One customer or `404` with message `"customer 999 not found"`. |
| `POST /customers` | Body `first_name`, `last_name`, `region` (non-empty), `email` (`x@y`), `plan` (`free`, `pro`, `enterprise`); header `Idempotency-Key` (required). `201` with the new `Customer`: id = max id + 1, `signup_date` from the `get_today` dependency, email stored trimmed and lowercased. |

## Rules

- **Pagination**: `page >= 1` (default 1); `page_size >= 1`, default and maximum come from `Settings` (`default_page_size`, `max_page_size`); a larger value is `422` naming `"query.page_size"`. `has_next` is true when more rows exist after this page.
- **Errors**: every non-2xx response from the app uses the envelope `{"error": {"code", "message", ...}}`: `not_found` (404), `conflict` (409), `http_error` (other HTTP errors such as 405), `validation_error` (422, `message` `"invalid request"`, extra `fields` like `["query.page"]`), `internal_error` (500, generic text, never the exception message). The health `503` is not an error envelope.
- **Idempotency**: the same key with the same body replays the original `201` response and creates nothing, even from a new app instance on the same database. The same key with a different body is `409`. Invalid requests (`422`) and rejected ones (duplicate email `409`) must not reserve the key. A duplicate email (case-insensitive) is `409`.
- **Config**: `get_settings` reads `REVENUE_DB_PATH`, `REVENUE_DEFAULT_PAGE_SIZE`, `REVENUE_MAX_PAGE_SIZE`, falling back to the defaults. Handlers get settings and connections through dependencies and open one connection per request.
- Use parameter placeholders for every value; never format request input into SQL.

## Rubric

- Correct reads: filters, ordering, rounding, totals and `has_next`
- Pagination limits driven by injected settings
- One consistent error envelope, no leaked internals
- Safe retries: idempotent POST that survives a restart
- Health endpoint that tells the truth
- Contract hygiene: no `email` in any response
