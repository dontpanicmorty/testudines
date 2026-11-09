`solution.py` has a handful of lint problems (unused import, bare `except`, comparison with `None`, unused variable, deprecated typing import, an assigned lambda, and more). Clean it up so that

```
python -m ruff check --select E,F,I,B,UP,SIM solution.py
```

reports nothing, **without changing what the functions do**:

- `read_config(path)` returns the parsed JSON, or `None` if the file is missing or invalid;
- `has_key(config, key)` is `True` only when `config` is not `None` and the key's value isn't `None`;
- `add_name(name)` appends to the module-level list `names`.

Don't add `# noqa` comments.
