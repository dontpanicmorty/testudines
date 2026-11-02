`Pipeline` collects error messages for a named pipeline. In production, a failure in the `orders` pipeline makes the `customers` pipeline report as failed too, even though it never recorded anything.

Fix the class so each pipeline tracks only its own errors. Behaviour to keep:

- `record_error(msg)` stores `"<pipeline name>: <msg>"`;
- `failed()` is `True` once at least one error has been recorded;
- `errors` is a list of the stored messages.

```python
a, b = Pipeline("orders"), Pipeline("customers")
a.record_error("timeout")
a.errors      # ['orders: timeout']
b.failed()    # False
```
