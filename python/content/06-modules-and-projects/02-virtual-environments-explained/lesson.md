+++
id = "modules-and-projects.virtual-environments-explained"
title = "Virtual environments, explained"
minutes = 25
+++

# Virtual environments, explained

Your dbt project pins its packages in `packages.yml` and records the exact resolved versions in `package-lock.yml`. Two engineers running `dbt deps` get the same macros. A Python **virtual environment** plus a lock file give you the same guarantee for Python libraries.

> **SQL bridge.** A dbt project with its own `dbt_packages/` folder ≈ a project with its own virtual environment. Without one, every project on your laptop shares one global pile of libraries, like every dbt project sharing one global `macros` folder.

## The problem: one Python, many projects

Project A needs `pandas 1.5`. Project B needs `pandas 2.2`. A single installation can only hold one version of a package at a time. Install for B and A breaks silently. An environment gives each project **its own private set of installed packages**.

## What a venv physically is

A virtual environment is just a **folder**. No magic, no daemon. It contains:

- a `pyvenv.cfg` text file that says which base Python it came from,
- a link to (or copy of) the Python interpreter,
- a `site-packages` directory where `pip install` puts libraries.

Let's build one right now, without pip so it's instant, and look inside:

```python
import tempfile
import venv
from pathlib import Path

root = Path(tempfile.mkdtemp()) / "demo-env"
venv.EnvBuilder(with_pip=False).create(root)

names = {p.name for p in root.iterdir()}
print("pyvenv.cfg" in names)

cfg = {}
for line in (root / "pyvenv.cfg").read_text().splitlines():
    key, _, value = line.partition("=")
    cfg[key.strip()] = value.strip()
print("home" in cfg, cfg["include-system-site-packages"])
```

"Activating" an environment only edits your shell's `PATH` so that `python` resolves to the one inside the folder. You can skip activation entirely by calling the environment's interpreter by path.

## How Python knows it's inside one

Two variables tell the story: `sys.base_prefix` is the original installation; `sys.prefix` is where the *current* environment lives. Inside a venv they differ.

```python
import sys

in_venv = sys.prefix != sys.base_prefix
print("running inside a venv:", in_venv)
print("same interpreter family:", sys.version_info[:2] >= (3, 12))
```

And `sys.path` (from the last lesson) includes the environment's `site-packages`, which is how `import pandas` finds the right copy:

```python
import sys
print([p for p in sys.path if p.endswith("site-packages")] != [])
```

You can also ask which version of an installed package you got:

```python
from importlib.metadata import version, PackageNotFoundError

for name in ["pytest", "not-a-real-package"]:
    try:
        print(name, "installed:", bool(version(name)))
    except PackageNotFoundError:
        print(name, "is not installed")
```

## Creating and using one (shell commands)

You run these in a terminal, so they are not runnable here:

```bash
# no-run
python -m venv .venv            # create the folder
source .venv/bin/activate       # put it first on PATH (Windows: .venv\Scripts\activate)
python -m pip install pandas    # installs into .venv/lib/.../site-packages
python -m pip freeze > frozen.txt
deactivate
```

Modern tools such as `uv` wrap these steps (`uv venv`, `uv add`, `uv sync`) and resolve far faster, but the folder they produce is the same kind of venv.

Rules of thumb: one environment per project; never commit the `.venv` folder (it is machine specific and rebuilt from a lock file); always install with `python -m pip` so the package lands in the interpreter you mean.

## Requirements versus lock files

Two different things people both call "the requirements":

| | What it states | Example line | Used for |
|---|---|---|---|
| **Requirements** (loose) | What the project *needs* | `pandas>=2.0` | Documenting intent, libraries |
| **Lock file** (exact) | What was *actually installed*, including dependencies of dependencies | `pandas==2.2.3` | Reproducing a run exactly |

A loose range is right for a library others will install alongside their own packages. An application or pipeline should deploy from a **lock file**, so that Monday's run and Friday's run use identical code. Without one, a new release of a transitive dependency can break a job that you never touched. That is the Python version of "the upstream source changed its schema overnight".

```python
def split_requirement(line):
    for op in ("==", ">=", "<=", "~=", ">", "<"):
        if op in line:
            name, _, version = line.partition(op)
            return name.strip(), op, version.strip()
    return line.strip(), None, None

print(split_requirement("pandas>=2.0"))
print(split_requirement("pandas==2.2.3"))
print(split_requirement("rich"))
```

## Reproducibility checklist

- Python version pinned (`requires-python`, or a `.python-version` file).
- Dependencies declared in `pyproject.toml` (next lessons).
- A lock file committed to version control.
- CI builds from the lock file, not from "whatever is latest today".

## Common mistakes

- Installing into the wrong Python: `ModuleNotFoundError: No module named 'pandas'` right after a successful `pip install`. Use `python -m pip` and check `sys.prefix`.
- Forgetting to activate (or to use the project's interpreter) in your editor.
- Committing `.venv` to git.
- Treating `pip freeze` output as hand-written requirements: it records everything, including packages you never asked for.

## What to take away

1. A venv is a folder with its own interpreter link and `site-packages`.
2. Activation only changes `PATH`; `sys.prefix != sys.base_prefix` tells you you're inside one.
3. Isolation lets projects use conflicting versions of a library.
4. Requirements state intent; lock files state the exact installed set.
5. Applications deploy from lock files so runs are reproducible.
