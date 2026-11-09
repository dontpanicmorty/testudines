`solution.py` is a small API over a store of invoices, protected by an `X-API-Key` header. The module exposes `app`, `get_store()` and `get_api_key()`.

Intended behavior:
- `GET /invoices/{invoice_id}` returns the invoice, or `404`.
- Requests without the right `X-API-Key` header get `401` (check the header against the value returned by `get_api_key()`), even for missing invoices.
- Tests replace `get_store` and `get_api_key` using `app.dependency_overrides`, so the real data never matters.

Right now the tests' fakes are ignored: the app keeps serving the built-in data and checking the built-in key. Fix `solution.py` so overriding works. Keep the names `app`, `get_store`, `get_api_key`.
