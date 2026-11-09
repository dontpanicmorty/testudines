Define `Session(log, name)`.

- When a session is created, it appends `"open <name>"` to the list `log`.
- When the session object is discarded (for example after `del s`), it appends `"close <name>"` to `log`.
- `name` is also available as an attribute.

```python
log = []
s = Session(log, "alpha")
del s
log      # ["open alpha", "close alpha"]
```
