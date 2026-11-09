In `datakit/deprecation.py`, implement `deprecated(use_instead, removed_in=None)`, a decorator factory.

A decorated function must:

- still return the original function's result for any arguments,
- emit a `DeprecationWarning` on each call whose message contains the old function's name and the text of `use_instead`, and, when given, `removed_in`,
- attribute the warning to the **caller's** file (`stacklevel=2`),
- keep its `__name__` and `__doc__`.

```python
@deprecated("load_rows", removed_in="2.0.0")
def read_rows(path):
    """Old name."""
    return load_rows(path)
```
