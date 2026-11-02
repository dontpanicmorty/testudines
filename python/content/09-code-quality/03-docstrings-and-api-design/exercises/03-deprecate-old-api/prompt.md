Your library is retiring old function names. Write the decorator `deprecated(replacement)`:

```python
@deprecated("total_cents")
def total(prices):
    """Add prices."""
    return sum(prices)

total([1, 2])    # returns 3, and warns the caller
```

Requirements:

- calling the decorated function emits a `DeprecationWarning` with exactly the message `"<function name> is deprecated; use <replacement>"`;
- the warning is attributed to the **caller's** file (use `stacklevel`), not to your decorator's;
- arguments (positional and keyword) pass through and the return value is unchanged;
- the wrapper keeps the original `__name__` and `__doc__`.
