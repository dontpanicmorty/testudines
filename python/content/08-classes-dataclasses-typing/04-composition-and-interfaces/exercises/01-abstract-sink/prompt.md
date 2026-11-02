Right now `Sink` is just a normal class, so nothing stops someone building a half-finished sink that fails later at run time. Make it an abstract base class and implement two sinks.

- `Sink` is abstract: `Sink()` raises `TypeError`, and so does a subclass that doesn't define `write`.
- `MemorySink().write(rows)` appends rows to its attribute `rows` and returns the number written.
- `CsvSink(path).write(rows)` writes the rows to the CSV file (header = keys of the first row; the file is rewritten on every call) and returns the number of rows. For an empty list it writes **nothing** (no file created) and returns `0`.

```python
sink = MemorySink()
sink.write([{"id": 1}, {"id": 2}])   # 2
sink.rows                            # [{'id': 1}, {'id': 2}]
```
