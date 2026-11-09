Implement `Pipeline` and `RunResult`. A pipeline is built from three callables:

- `extract()` returns an iterable of rows (dicts);
- `transform(row)` returns the cleaned row, or `None` to reject it. If it raises `ValueError`, the row is also rejected; any other exception propagates;
- `load(rows)` receives the list of cleaned rows and returns how many it stored.

`Pipeline(extract, transform, load).run()` returns a frozen dataclass `RunResult(rows_in, rows_out, rejected)`: rows extracted, the number `load` returned, and rows rejected. `load` is called **exactly once**, even with an empty list, and sees rows in extraction order.

```python
p = Pipeline(lambda: [{"n": "1"}, {"n": "x"}, {"n": "3"}],
             lambda r: {"n": int(r["n"])},
             lambda rows: len(rows))
p.run()   # RunResult(rows_in=3, rows_out=2, rejected=1)
```
