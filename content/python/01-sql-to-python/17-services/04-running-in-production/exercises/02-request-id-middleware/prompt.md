Write `add_request_id(app)` which installs a middleware on a FastAPI app:

1. Use the incoming `X-Request-ID` header if present and non-empty, otherwise generate a fresh id (`uuid.uuid4().hex`).
2. Make it available to handlers as `request.state.request_id`.
3. Return it on **every** response in the `X-Request-ID` header, including error responses such as 404 and 422.
4. Emit exactly one record per request on the logger named `"access"` at INFO level, message `"request"`, with `extra={"fields": {...}}` containing `request_id`, `method`, `path`, `status` (int) and `duration_ms` (float >= 0).
5. If a handler raises an unexpected exception, log the record with `status` 500 and let the exception propagate.

```python
app = FastAPI()
add_request_id(app)
client.get("/ping", headers={"X-Request-ID": "abc"}).headers["x-request-id"]   # "abc"
```
