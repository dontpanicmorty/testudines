Write `load_module_from(directory, name)`, a loader for pipeline plugins. It imports the module called `name` from `directory` and returns it.

Requirements:

- The function must leave `sys.path` exactly as it found it, even when the import raises.
- Two different directories may each contain a `plugin.py`. Loading them one after the other must give each its own code (don't return a stale cached module).
- The module must not remain in `sys.modules` afterwards.
- If the module doesn't exist, let the `ModuleNotFoundError` propagate.

```python
mod = load_module_from("/tmp/team_a", "plugin")
print(mod.run())
```
