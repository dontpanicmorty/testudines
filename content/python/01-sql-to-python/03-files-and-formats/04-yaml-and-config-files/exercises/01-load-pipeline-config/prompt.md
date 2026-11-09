`load_config(path)` reads a YAML file and returns a dict with these keys always present:

- `name` (required; raise `KeyError("name")` if missing),
- `retries` (default `3`),
- `sources` (default `[]`).

Other keys in the file are kept as they are.

```python
# file: name: daily\nretries: 5\nowner: data-eng
load_config(path)   # {"name": "daily", "retries": 5, "sources": [], "owner": "data-eng"}
```
