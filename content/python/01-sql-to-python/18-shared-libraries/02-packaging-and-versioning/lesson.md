+++
id = "shared-libraries.packaging-and-versioning"
title = "Packaging and versioning"
minutes = 35
+++

# Packaging and versioning

You have installed dbt packages by listing a name and a version in `packages.yml`. For Python the equivalent is a project with a `pyproject.toml` that describes itself, and a **wheel** that other people install. This lesson covers what is inside both.

> **dbt bridge.** `packages.yml` says `version: [">=1.0.0", "<2.0.0"]`. Every package you consume promises that `1.x` will not break you. Now you will be the one making that promise, so you need to understand semantic versioning and what the number means.

## pyproject.toml

One TOML file declares the project: name, version, Python requirement, dependencies and how to build it.

```python
import tomllib

PYPROJECT = """
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "acme-datakit"
version = "1.4.2"
description = "Shared data helpers for the analytics team"
requires-python = ">=3.10"
dependencies = ["pydantic>=2,<3"]

[project.optional-dependencies]
pandas = ["pandas>=2"]
dev = ["pytest", "ruff"]

[project.scripts]
datakit = "acme_datakit.cli:main"
"""

meta = tomllib.loads(PYPROJECT)
print(meta["project"]["name"], meta["project"]["version"])
print(meta["project"]["dependencies"])
print(sorted(meta["project"]["optional-dependencies"]))
```

`tomllib` is in the standard library, so reading TOML is free. Note the **distribution name** (`acme-datakit`, what you `pip install`) differs from the **import name** (`acme_datakit`, what you `import`). Hyphens are not valid in Python identifiers.

## Semantic versioning

A version is `MAJOR.MINOR.PATCH`:

| Bump | When | Consumer impact |
|---|---|---|
| PATCH `1.4.2 -> 1.4.3` | bug fix, no API change | safe to take |
| MINOR `1.4.2 -> 1.5.0` | new backward-compatible feature | safe to take |
| MAJOR `1.4.2 -> 2.0.0` | anything that can break callers | read the notes first |

Bumping resets the lower parts to zero.

> **Predict first.** What is the next version after `1.4.2` for: a new optional parameter? A renamed function? A typo fix?

```python
def bump(version, part):
    major, minor, patch = (int(p) for p in version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"

print(bump("1.4.2", "minor"), bump("1.4.2", "major"), bump("1.4.2", "patch"))
```

Never compare versions as strings: `"1.10.0" < "1.9.0"` is `True`. Compare tuples of ints:

```python
print("1.10.0" < "1.9.0")
print((1, 10, 0) < (1, 9, 0))
```

Versions starting with `0.` signal "anything may change". Move to `1.0.0` when you accept responsibility for stability.

## Changelogs

A changelog tells consumers what changed in each version, written for humans. Group entries by kind: Added, Changed, Deprecated, Removed, Fixed. Newest version first. Write it as you merge, not at release time when you have forgotten.

```
## [1.5.0] - 2026-02-01
### Added
- `summarize(..., top_n=)` option.
### Fixed
- `parse_amount` no longer fails on trailing spaces.
```

## A wheel is a zip

Building produces a **wheel**, a `.whl` file. It is a plain zip archive containing your package files and a `*.dist-info/` folder of metadata. Installing a wheel is mostly unzipping it into `site-packages`. We can build a toy one with `zipfile`, offline, to see exactly what is inside:

```python
import tempfile, zipfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    pkg = d / "src" / "acme_datakit"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text('__version__ = "1.4.2"\n')
    (pkg / "core.py").write_text("def hello():\n    return 'hi'\n")

    wheel = d / "acme_datakit-1.4.2-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as zf:
        for f in sorted(pkg.rglob("*.py")):
            zf.write(f, f.relative_to(d / "src").as_posix())
        zf.writestr(
            "acme_datakit-1.4.2.dist-info/METADATA",
            "Metadata-Version: 2.1\nName: acme-datakit\nVersion: 1.4.2\n",
        )

    with zipfile.ZipFile(wheel) as zf:
        for name in zf.namelist():
            print(name)
        print(zf.read("acme_datakit-1.4.2.dist-info/METADATA").decode())
```

The file name encodes `{name}-{version}-{python tag}-{abi tag}-{platform tag}`. `py3-none-any` means pure Python, runs anywhere. A real build tool also writes `WHEEL` and `RECORD` files, but the idea is the same. When a consumer reports a missing file, listing the wheel's contents is the first thing to do.

## Optional dependencies and entry points

**Extras** keep the base install light. `pip install "acme-datakit[pandas]"` adds the packages listed under `pandas`. Your code imports them lazily and gives a helpful error if absent:

```python
def to_frame(rows):
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "to_frame needs pandas: install acme-datakit[pandas]"
        ) from exc
    return pd.DataFrame(rows)

print(to_frame([{"a": 1}]).shape)
```

**Entry points** turn a function into a command. In the pyproject above, `datakit = "acme_datakit.cli:main"` creates a `datakit` executable that imports `acme_datakit.cli` and calls `main()`. The text format is `module.path:function`:

```python
def parse_entry_point(spec):
    module, func = spec.split(":")
    return module, func

print(parse_entry_point("acme_datakit.cli:main"))
```

## Common mistakes

- Forgetting to bump the version before release, so the index rejects the upload or consumers get stale code.
- Distribution name and import name drift apart and confuse everyone.
- Unbounded dependencies (`pydantic`) that break you when a new major arrives; pin a sensible range.
- Putting test-only tools in `dependencies` instead of an extra.
- `ModuleNotFoundError: No module named 'acme_datakit'` because the package directory is missing `__init__.py` or was not included in the build.

## What to take away

1. `pyproject.toml` declares name, version, dependencies, extras and scripts.
2. SemVer: patch for fixes, minor for compatible features, major for breaks. Compare versions as int tuples.
3. Keep a changelog grouped by kind, newest first.
4. A wheel is a zip of your package plus `dist-info` metadata; inspect it with `zipfile`.
5. Extras keep the base light; entry points expose functions as commands.
