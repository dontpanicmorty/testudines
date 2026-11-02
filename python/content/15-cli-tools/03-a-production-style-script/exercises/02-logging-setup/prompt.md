Write `setup_logging(verbose=False, stream=None)`; it configures and returns the logger named `"jobrunner"`:

- level `DEBUG` if `verbose` else `INFO`;
- exactly **one** `StreamHandler` writing to `stream` (default `sys.stderr`), formatted `LEVEL name: message`, e.g. `INFO jobrunner: loaded 3 rows`;
- calling it again replaces the handler (the new `stream` takes effect and nothing is printed twice);
- the logger does not propagate to the root logger.

```python
log = setup_logging(verbose=True, stream=buf)
log.debug("x=%d", 1)     # buf: "DEBUG jobrunner: x=1\n"
```
