Write `make_logger(name, path, level=logging.INFO)` that returns a `logging.Logger` which writes to the file at `path` (UTF-8) in the format `LEVEL | name | message`, e.g. `INFO | etl.run | started`.

- Records below `level` are dropped.
- Calling `make_logger` again with the same name must **not** add a second handler (no duplicated lines).
- Records must not propagate to the root logger.

```python
log = make_logger("etl.run", Path("run.log"))
log.info("started")
```
