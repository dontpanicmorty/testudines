Write `summarize_pyproject(text)` that parses pyproject TOML text and returns a dict:

```python
{
  "name": "acme-datakit",
  "version": "1.4.2",
  "dependencies": ["pydantic>=2,<3"],            # [] if absent
  "extras": ["dev", "pandas"],                   # sorted names, [] if absent
  "scripts": {"datakit": ("acme_datakit.cli", "main")},   # {} if absent
}
```

Each script value `"module.path:function"` becomes a `(module, function)` tuple. Raise `ValueError` if `[project]` lacks `name` or `version`, or a script spec has no `:`.

Use the standard library `tomllib`.
