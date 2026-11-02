+++
id = "cli-tools.a-production-style-script"
title = "A production-style script"
minutes = 30
+++

# A production-style script

A script that works on your laptop once is not a job you can leave running. A production job answers a short checklist: *Where do settings come from? What does it log? What happens to bad rows? How does the scheduler know it failed? Can I run it in a test?* This lesson assembles the previous lessons (settings, logging, argparse, exit codes, validation) into one robust shape.

> **dbt bridge.** A dbt run has a project config, a log, per-model pass/fail, and a final exit code. Same anatomy, different tool.

## The shape

```
jobrunner/
  config.py     settings from env (+ CLI overrides), validated up front
  validate.py   pure functions: row -> list of problems
  runner.py     the pipeline: read, validate, write good + rejected rows
  logs.py       logging setup
  cli.py        main(argv, env) -> exit code: the thin outer layer
```

Each layer has one job and can be tested alone. `cli.py` is the only file that knows about argparse, `sys` and exit codes.

## Layer 1: configuration, validated before any work

```python
from collections.abc import Mapping
from dataclasses import dataclass

class ConfigError(Exception):
    pass

@dataclass(frozen=True)
class JobConfig:
    input_path: str
    max_error_rate: float = 0.1

def load_config(env: Mapping[str, str]) -> JobConfig:
    problems = []
    if "JOB_INPUT" not in env:
        problems.append("JOB_INPUT is required")
    try:
        rate = float(env.get("JOB_MAX_ERROR_RATE", "0.1"))
        if not 0 <= rate <= 1:
            raise ValueError
    except ValueError:
        problems.append("JOB_MAX_ERROR_RATE must be a number between 0 and 1")
        rate = 0.1
    if problems:
        raise ConfigError("; ".join(problems))
    return JobConfig(env["JOB_INPUT"], rate)

print(load_config({"JOB_INPUT": "orders.csv"}))
try:
    load_config({"JOB_MAX_ERROR_RATE": "7"})
except ConfigError as e:
    print("config error:", e)
```

Collect **all** problems before raising, so the operator fixes everything in one go.

## Layer 2: validation as pure functions

A validator takes one row and returns a list of problems (empty means fine). No printing, no files: trivially testable and reusable.

```python
def validate_row(row: dict) -> list[str]:
    problems = []
    try:
        if int(row.get("order_id", "")) <= 0:
            problems.append("order_id: must be positive")
    except ValueError:
        problems.append("order_id: not an integer")
    try:
        if float(row.get("amount", "")) < 0:
            problems.append("amount: negative")
    except ValueError:
        problems.append("amount: not a number")
    return problems

print(validate_row({"order_id": "7", "amount": "19.5"}))
print(validate_row({"order_id": "x", "amount": "-1"}))
```

## Layer 3: quarantine, don't crash and don't hide

Real exports contain bad rows. Crashing on row 90,000 wastes the run; silently dropping bad rows loses data. The standard answer: write good rows to the output, bad rows with their **reason** to a rejects file, and count both. Then decide with an **error budget**: tolerate up to N% bad rows, fail beyond that.

```python
def split_rows(rows):
    good, rejected = [], []
    for row in rows:
        problems = validate_row(row)
        if problems:
            rejected.append({**row, "reason": "; ".join(problems)})
        else:
            good.append(row)
    return good, rejected

def validate_row(row):
    return [] if row["amount"].replace(".", "", 1).isdigit() else ["amount: not a number"]

good, bad = split_rows([{"amount": "5"}, {"amount": "x"}, {"amount": "7.5"}])
print(len(good), len(bad), bad[0]["reason"])
print("error rate:", len(bad) / (len(good) + len(bad)))
```

## Layer 4: logging

Use the `logging` module, not `print`, for diagnostics: levels, timestamps, one place to redirect. Logs go to **stderr**; the final summary line goes to stdout. Configure logging **once**, in the entry point, never at import time in library code.

```python
import logging
import sys

def setup_logging(verbose: bool) -> logging.Logger:
    log = logging.getLogger("jobrunner")
    log.handlers.clear()                     # safe if called twice
    handler = logging.StreamHandler(sys.stdout)   # stdout here only so the demo prints it
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    log.propagate = False
    return log

log = setup_logging(verbose=False)
log.debug("hidden")
log.info("loaded %d rows", 120)
log.warning("rejected %d rows", 3)
```

(In the real job the handler writes to `sys.stderr`.) Pass values as `%d` arguments rather than pre-formatting with f-strings: it is cheaper when the level is off. Never log secrets (see the settings lesson).

## Layer 5: main returns a meaningful exit code

```python
def decide(total: int, rejected: int, max_rate: float) -> int:
    if total == 0:
        return 1                          # an empty input is suspicious
    return 0 if rejected / total <= max_rate else 1

print(decide(100, 5, 0.1), decide(100, 20, 0.1), decide(0, 0, 0.1))
```

A documented set of codes keeps the scheduler honest:

| Code | Meaning |
|---|---|
| 0 | success, within the error budget |
| 1 | ran, but too many bad rows (or empty input) |
| 2 | invalid configuration or usage |
| 3 | input file missing or unreadable |

The outer `main` catches the *expected* exceptions (`ConfigError`, `FileNotFoundError`), maps each to a code and a one-line message on stderr, and lets genuine bugs surface as tracebacks.

## Testing the assembled job

Because settings come from a mapping, streams are injectable and `main` returns a code, a full end-to-end test is a normal function: write a small CSV into `tmp_path`, call `main([...], env={...})`, assert on the code, the output files and the captured output. No subprocess, no network, no clock.

## Common mistakes

- Configuring logging at import time, so importing the module in a test changes global logging.
- `except Exception: return 0` around the whole job: failures vanish.
- Dropping bad rows without a rejects file or count.
- Validating inside the loop with `print`: you cannot test it and it cannot be reused.
- Reading `os.environ` all over the code instead of once in `load_config`.
- Adding a log handler on every call to `setup_logging`, which prints each message twice.

## What to take away

1. Layer the job: config, validation, pipeline, logging, then a thin `main`.
2. Validate settings up front and report every problem at once.
3. Keep validators pure; quarantine bad rows with reasons; enforce an error budget.
4. Configure logging once, in the entry point; logs to stderr, the result to stdout.
5. Map expected failures to documented exit codes; let bugs crash visibly.
