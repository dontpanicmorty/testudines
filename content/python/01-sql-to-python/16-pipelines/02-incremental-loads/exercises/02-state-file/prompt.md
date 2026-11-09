Build the state storage for an incremental job from scratch. Write two functions in `solution.py`:

- `load_state(path)` returns a dict. If the file does not exist it returns `{"watermark": None}`. If the file exists, return its JSON content, but make sure a `"watermark"` key is always present (default `None`).
- `save_state(path, state)` writes the dict as JSON **atomically** (temp file in the same directory, then `os.replace`). The parent directory may not exist yet, so create it. No temp files may be left next to the state file.

```python
save_state("state/orders.json", {"watermark": "2026-01-02T00:00:00"})
load_state("state/orders.json")   # {"watermark": "2026-01-02T00:00:00"}
```
