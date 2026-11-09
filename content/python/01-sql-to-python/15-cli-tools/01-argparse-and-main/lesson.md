+++
id = "cli-tools.argparse-and-main"
title = "argparse and the main(argv) pattern"
minutes = 25
+++

# argparse and the main(argv) pattern

A pipeline job is a program someone (a scheduler, a teammate, you at 2 a.m.) runs with different inputs. In dbt you have `dbt run --select tag:daily --target prod`: flags, defaults, help text, and a non-zero exit when something fails. Python scripts deserve the same, and the standard library's `argparse` provides it.

> **dbt bridge.** `--select`, `--target`, `--full-refresh` are options and flags; `dbt run` exiting non-zero is what makes the orchestrator mark the task failed.

## Why not `sys.argv` directly

```python
import sys
print(sys.argv)
```

`sys.argv` is a raw list of strings: you would hand-write parsing, type conversion, defaults, help and error messages. `argparse` does all of that.

## Defining arguments

```python
import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="load_orders", description="Load an orders export.")
    p.add_argument("path", help="CSV file to load")                      # positional, required
    p.add_argument("--env", choices=["dev", "prod"], default="dev")      # option with allowed values
    p.add_argument("--batch-size", type=int, default=500)                # converted to int
    p.add_argument("--dry-run", action="store_true")                     # flag: False unless given
    return p

args = build_parser().parse_args(["orders.csv", "--batch-size", "100", "--dry-run"])
print(args)
print(args.path, args.batch_size, args.dry_run, args.env)
```

Notes: `--batch-size` becomes `args.batch_size`; `type=int` converts and rejects `abc`; `store_true` makes a flag; `choices` validates.

> **Predict first.** What happens if you pass `--env staging`?

```python
import argparse, contextlib, io

p = argparse.ArgumentParser(prog="job")
p.add_argument("--env", choices=["dev", "prod"], default="dev")

err = io.StringIO()
try:
    with contextlib.redirect_stderr(err):
        p.parse_args(["--env", "staging"])
except SystemExit as e:
    print("exit code:", e.code)
print(err.getvalue().strip().splitlines()[-1])
```

argparse prints a usage error to **stderr** and raises `SystemExit(2)`. By convention, exit code 2 means "you invoked it wrongly".

## The main(argv) pattern

A script that does everything at import time cannot be tested or reused. Instead:

```python
import argparse
import sys
from collections.abc import Sequence

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="count")
    parser.add_argument("numbers", nargs="+", type=int)
    args = parser.parse_args(argv)          # argv=None means "use sys.argv[1:]"
    print(sum(args.numbers))
    return 0

print("returned", main(["1", "2", "3"]))
```

```python
# no-run
if __name__ == "__main__":
    sys.exit(main())
```

Three ideas:

1. `main` takes `argv` so tests call `main(["--flag", "x"])` with no subprocess.
2. `main` **returns** an exit code instead of calling `sys.exit` itself. Only the `__main__` guard exits.
3. Importing the module does nothing; the guard stops `main()` from running on import.

## Exit codes

The exit code is how the outside world learns what happened. Zero is success; non-zero is failure. Pick a small, documented set:

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | the job ran and failed (bad data, I/O error) |
| 2 | bad command line (argparse uses this) |

## stdout vs stderr

**stdout** is for the program's *result* (data someone may pipe into another tool). **stderr** is for diagnostics: progress, warnings, errors. Mixing them breaks pipelines: an error message in stdout becomes a row in the next tool's input.

```python
import sys

def report(count: int) -> None:
    print(count)                                   # result -> stdout
    print("done in 0.2s", file=sys.stderr)         # diagnostics -> stderr

report(3)
```

## Failing cleanly

```python
import argparse
import sys
from pathlib import Path

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="rowcount")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        text = args.path.read_text()
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc.strerror}", file=sys.stderr)
        return 1
    print(len([ln for ln in text.splitlines() if ln.strip()]))
    return 0

print("exit code:", main(["/definitely/missing.csv"]))
```

A traceback is for programmers; users need one clear line and a non-zero code. Catch the **expected** failures (`OSError`, your own `DataError`) and let real bugs crash loudly.

## Injecting the streams

To test output without capturing the real terminal, accept streams as parameters with defaults:

```python
import io
import sys

def main(argv, *, stdout=None, stderr=None) -> int:
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    if not argv:
        print("error: no input", file=stderr)
        return 2
    print(" ".join(argv), file=stdout)
    return 0

out, err = io.StringIO(), io.StringIO()
print(main(["a", "b"], stdout=out, stderr=err), repr(out.getvalue()), repr(err.getvalue()))
print(main([], stdout=out, stderr=err), repr(err.getvalue()))
```

pytest's `capsys` fixture gives you the same ability; both work because the function never hard-codes its streams.

## Common mistakes

- Running the program at import time (no `__main__` guard): importing it in a test starts the job.
- `sys.exit(0)` buried deep inside helper functions; they become impossible to reuse. Return values, and exit once at the top.
- Errors printed to stdout, then piped into the next step as data.
- Always returning `0`, so the scheduler reports green when the load failed.
- `type=bool` for flags: `bool("False")` is `True`. Use `action="store_true"`.
- `error: argument --batch-size: invalid int value: 'abc'`: that is argparse working as intended; don't catch it.

## What to take away

1. argparse turns `sys.argv` strings into typed, validated, documented options.
2. `main(argv=None) -> int` plus a `__main__` guard makes a script importable and testable.
3. Exit 0 for success, non-zero for failure; let argparse own code 2.
4. Results to stdout, diagnostics and errors to stderr.
5. Catch expected errors and print one clear line; do not hide bugs.
