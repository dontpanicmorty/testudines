Every error from the service should look the same:

```json
{"error": {"code": "not_found", "message": "order 5 not found"}}
```

Write `install_error_handlers(app)` in `solution.py` that registers handlers on an existing `FastAPI` app so that:

| Situation | status | `code` | `message` |
|---|---|---|---|
| `HTTPException` (any status, including unknown routes) | same as exception | `not_found` for 404, `conflict` for 409, `http_error` otherwise | the exception detail as text |
| request validation fails | 422 | `validation_error` | `"invalid request"`, plus an extra key `fields`: list of dotted locations like `"query.limit"` or `"body.items.0.quantity"` |
| any other exception | 500 | `internal_error` | `"internal server error"` (never the exception text) |

```python
app = FastAPI()
install_error_handlers(app)
```
