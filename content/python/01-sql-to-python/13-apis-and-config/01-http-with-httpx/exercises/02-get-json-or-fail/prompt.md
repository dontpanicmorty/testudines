`get_json(client, path)` is meant to return the parsed JSON body for successful calls and to raise `ApiError` otherwise. `ApiError` has a `status_code` attribute (`None` when no response arrived, e.g. a timeout).

Right now a `503` with a JSON error body comes back to the caller as if it were good data, and a pipeline built on it would load garbage. Fix the function so that:

- 2xx returns the parsed JSON
- any other status raises `ApiError(status_code=<that status>)`
- timeouts and other transport failures raise `ApiError(status_code=None)`

```python
get_json(client, "/users/1")    # {"id": 1, ...}
get_json(client, "/boom")       # raises ApiError, .status_code == 500
```
