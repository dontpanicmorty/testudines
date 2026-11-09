+++
id = "code-quality.linting-and-formatting"
title = "Linting and formatting"
minutes = 25
+++

# Linting and formatting

If you've used **sqlfluff** on a dbt project you know the idea: a tool reads your code, reports style problems and real mistakes, and fixes many of them automatically. In Python the tool is **ruff**. It is one fast program that does two jobs: a **linter** (`ruff check`) that finds problems, and a **formatter** (`ruff format`) that rewrites layout.

> **SQL bridge.** `sqlfluff lint` ≈ `ruff check`; `sqlfluff fix` ≈ `ruff check --fix` and `ruff format`. Your team's `.sqlfluff` config ≈ the `[tool.ruff]` table in `pyproject.toml`.

## Linting: it finds bugs, not just style

Run ruff on a deliberately sloppy snippet. This helper writes the code to a temp file and runs ruff with a chosen set of rules:

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def ruff(source, *args):
    folder = Path(tempfile.mkdtemp())
    (folder / "snippet.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "ruff", *args, "--isolated", "snippet.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip())

ruff('''
import os
import sys, json
from typing import List

def load(path, cache={}):
    try:
        data = json.load(open(path))
    except:
        return None
    unused = len(data)
    if data == None:
        return []
    return data
''', "check", "--no-cache", "--select", "E,F,I,B,UP", "--output-format", "concise")
```

Each line is `file:line:col: CODE message`. The letter prefix says which family of rules:

| Code | Family | Catches |
|---|---|---|
| `F` | pyflakes | unused imports/variables, undefined names (`F401`, `F841`) |
| `E` / `W` | pycodestyle | PEP 8 layout and style problems (`E711`, `E722`) |
| `I` | isort | unsorted or messy imports (`I001`) |
| `B` | bugbear | likely bugs: mutable defaults, late-binding closures (`B006`, `B023`) |
| `UP` | pyupgrade | outdated syntax (`typing.List` instead of `list`) |
| `SIM` | simplify | needlessly complicated code |

Look at what these found beyond style. A **mutable default** (`cache={}`, `B006`) is shared across calls, a real bug. A **bare `except:`** (`E722`) swallows `KeyboardInterrupt` and hides mistakes. An **unused variable** (`F841`) often means a result was computed and forgotten. `== None` (`E711`) should be `is None`. This is why linting is more than taste.

Fix what ruff reports, and let it do the mechanical part: `ruff check --fix` removes unused imports and sorts them. "Unsafe" fixes are suggestions you review yourself.

## PEP 8 essentials

PEP 8 is Python's style convention. You don't need to memorise it because ruff enforces it, but know the shape:

- `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_SNAKE` for constants.
- 4 spaces per indent level, never tabs mixed in.
- Two blank lines between top-level functions, one between methods.
- Imports at the top, grouped: standard library, third party, your own; one per line.
- Compare with `None` using `is`, not `==`.
- Lines about 88-100 characters at most.
- Don't write `if flag == True:`; write `if flag:`.

## Formatting is not a debate

Arguments about quote style or where to break a line waste time and make diffs noisy. A **formatter** ends the argument: one tool, one output, run on save or in CI. Nobody has to review or discuss layout again.

```python
import subprocess, sys, tempfile, textwrap
from pathlib import Path

def ruff(source, *args):
    folder = Path(tempfile.mkdtemp())
    (folder / "snippet.py").write_text(textwrap.dedent(source))
    cmd = [sys.executable, "-m", "ruff", *args, "--isolated", "snippet.py"]
    r = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip())

ruff('''
x = {  "a":1,'b':2 }
def f( a,b ):
    return a+b
''', "format", "--diff")
```

The formatter changed spacing, quotes and blank lines, and nothing about behaviour. In the terminal you run `python -m ruff format .` to apply it, or `python -m ruff format --check .` in CI to fail when something isn't formatted.

## Configuring ruff

Put the rules your team agreed on in `pyproject.toml`, so everyone and CI gets identical results:

```toml
# no-run
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = ["E501"]      # an example: don't police line length
```

Start with a modest set (`E`, `F`, `I`, `B`, `UP`), add more later. Suppress an individual false positive with a comment, giving a reason: `x = compute()  # noqa: F841 (kept for debugging)`. Never blanket-disable rules.

## A good workflow

1. Editor shows ruff warnings as you type.
2. On save (or pre-commit): `ruff check --fix` then `ruff format`.
3. CI runs `ruff check .` and `ruff format --check .`, together with the tests and `mypy`.

## Common mistakes

- Ignoring warnings until there are 400 of them. Keep the project clean from day one.
- Fixing lint noise in the same commit as a behaviour change. Separate them so reviewers can read the diff.
- Using `# noqa` everywhere instead of fixing. If you add one, say why.
- Debating formatting in code review. Run the formatter and move on.
- Turning on every rule at once on an old codebase. Add rule families gradually.

## What to take away

1. `ruff check` lints (finds bugs and style problems); `ruff format` formats.
2. Rule codes have a letter family: F (pyflakes), E (style), I (imports), B (likely bugs), UP (modern syntax).
3. Many hits are real bugs: mutable defaults, bare `except`, unused results.
4. A formatter ends layout debates; run it automatically.
5. Configure rules in `pyproject.toml` and run the same checks locally and in CI.
