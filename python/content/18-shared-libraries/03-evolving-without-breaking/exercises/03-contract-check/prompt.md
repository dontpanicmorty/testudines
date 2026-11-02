A consumer team gives you their expectations of `datakit.parse_amount` as data. Write `check_contract(func, cases)` in `contract.py`; `cases` is a list of `(args, kwargs, expected)` tuples.

Return a list of failure messages, one per failing case, in order; an empty list means the contract holds.

- A case fails when `func(*args, **kwargs)` returns something `!= expected`: message `"case N: expected X, got Y"` (N is the 0-based index; X and Y use `repr`).
- A case fails when it raises: message `"case N: raised TypeName"`.
- If `expected` is an exception class, the case passes only if that exception is raised; a normal return fails with `"case N: expected TypeName to be raised"`.

```python
check_contract(parse_amount, [(("$5",), {}, 5.0), (("x",), {}, ValueError)])   # []
```

`library.py` is provided as the library under test.
