Write `check_release(project_dir)` that inspects a project folder and returns a list of problem codes (empty list means ready to release). `project_dir` is a `Path` or string. The layout is:

```
project/
  pyproject.toml          # [project] name = "acme-datakit", version = "1.5.0"
  README.md
  CHANGELOG.md
  src/acme_datakit/__init__.py   # contains __version__ = "1.5.0"
```

Report, in this order, each at most once:

1. `"missing_readme"`: no `README.md`.
2. `"missing_changelog"`: no `CHANGELOG.md`.
3. `"changelog_version"`: the changelog exists but has no heading line starting with `## [<version>]` for the pyproject version.
4. `"version_mismatch"`: `__version__` in `src/<import_name>/__init__.py` (import name = project name with `-` replaced by `_`) differs from the pyproject version, or the file/attribute is missing.

If `pyproject.toml` is missing or has no `[project].version`, return just `["no_version"]`.
