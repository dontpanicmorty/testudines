Write two helpers a support script could use to print an environment report.

`describe_environment()` returns a dict with exactly these keys:

- `"in_venv"`: `True` when running inside a virtual environment (`sys.prefix` differs from `sys.base_prefix`);
- `"python"`: the version as `"MAJOR.MINOR"`, e.g. `"3.12"`;
- `"has_site_packages"`: `True` if any entry on `sys.path` ends with `site-packages` or `dist-packages`.

`installed_version(package)` returns the installed version string of a package, or `None` if it isn't installed.

```python
describe_environment()          # {'in_venv': True, 'python': '3.12', 'has_site_packages': True}
installed_version("pytest")     # '8.3.4'
installed_version("nope-xyz")   # None
```
