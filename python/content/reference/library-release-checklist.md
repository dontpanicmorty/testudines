# Library release checklist

## Before you change the API

| Change | Breaking? | Version bump |
|---|---|---|
| bug fix | no | patch |
| new function or optional keyword-only parameter | no | minor |
| new required parameter, rename, removal, reorder | yes | major |
| behaviour or exception change | yes | major (or flag it) |

Deprecate first:

```python
warnings.warn("old is deprecated, use new (removed in 2.0.0)",
              DeprecationWarning, stacklevel=2)
```

## Release steps

1. Tests, lint and type checks pass on main.
2. Choose the bump from the changelog.
3. Update the version in `pyproject.toml` (and `__version__` if kept).
4. Move Unreleased entries under `## [x.y.z] - date`.
5. Build the wheel; list it with `zipfile` and check the contents.
6. Tag `vX.Y.Z` and publish. Never move a published tag.
7. Announce deprecations and breaking changes.

## Library health

- Public API: `__all__` in `__init__.py`, underscore for private.
- Dependencies: minimal, optional ones as extras and imported lazily.
- Docs: docstrings with doctest examples; README with install and quick start.
- Contract tests pin behaviour consumers rely on.

## Consuming

```python
# no-run
# pip install "acme-datakit>=1.4,<2"
# pip install "acme-datakit @ git+https://git.internal.example/data/datakit.git@v1.4.2"
```
