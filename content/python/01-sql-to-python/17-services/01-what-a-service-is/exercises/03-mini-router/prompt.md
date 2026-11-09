Frameworks route a request to a handler by method and path pattern. Build the core of that idea.

Implement a class `Router` in `solution.py`:

- `add(method, pattern, handler)` registers a route. Patterns look like `/orders/{order_id}`; `{name}` captures one path segment.
- `dispatch(method, path)` finds the route and calls `handler(**params)` with the captured segments (as strings), returning whatever the handler returns.
- No pattern matches the path: return `(404, {"error": "not found"})`.
- A pattern matches the path but not with that method: return `(405, {"error": "method not allowed"})`.
- Methods are case-insensitive. A trailing slash on the request path is ignored.
- A literal route wins over a placeholder route when both match (`/orders/recent` beats `/orders/{order_id}`).

```python
r = Router()
r.add("GET", "/orders/{order_id}", lambda order_id: (200, {"id": order_id}))
r.dispatch("get", "/orders/1001")    # (200, {"id": "1001"})
r.dispatch("POST", "/orders/1001")   # (405, {"error": "method not allowed"})
r.dispatch("GET", "/nope")           # (404, {"error": "not found"})
```
