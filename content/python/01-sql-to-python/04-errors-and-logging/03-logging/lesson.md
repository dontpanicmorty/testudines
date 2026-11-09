+++
id = "errors-and-logging.logging"
title = "Logging"
minutes = 30
+++

# Logging

When a nightly job fails at 3 a.m., the only witness is what it wrote down. In a warehouse you have `QUERY_HISTORY` and task run logs. In Python **you** decide what gets recorded, and the `logging` module is the standard way to do it.

> **SQL bridge.** Query history records what ran, when, for how long, and whether it failed. A good log line does the same for your code: *what* happened, *to which entity*, and *how much*.

## Why `print` is not logging

`print` writes text to stdout. Nothing more. No timestamp, no severity, no way to silence it, redirect it to a file, or ship it to a log service without editing the code. Library code that prints forces its noise on every caller.

Logging gives you **levels**, **formatting**, and **destinations** that the application configures once, while libraries only emit records.

## Levels

From least to most severe: `DEBUG` (10), `INFO` (20), `WARNING` (30), `ERROR` (40), `CRITICAL` (50).

| Level | Use for |
|---|---|
| DEBUG | detail useful only while diagnosing |
| INFO | normal milestones: "loaded 1,204 rows" |
| WARNING | something odd, but the run continues: "12 rows rejected" |
| ERROR | an operation failed |
| CRITICAL | the whole program cannot continue |

A logger only passes records at or above its **level**. The default is WARNING, which is why `logger.info(...)` often seems to do nothing.

## A first logger

```python
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
    force=True,
)
log = logging.getLogger("etl.load")

log.debug("not shown, below INFO")
log.info("loaded %d rows", 1204)
log.warning("rejected %d rows", 12)
log.error("target table %s is locked", "orders")
```

Note `log.info("loaded %d rows", 1204)`, not an f-string. The logging module only formats the message **if the record is actually emitted**, and tools can group records by the unformatted template. Use `%s`-style arguments.

`basicConfig` is for application entry points and scripts. Libraries must never call it.

## One logger per module

```python
import logging

log = logging.getLogger(__name__)   # at the top of every module
```

`__name__` is the module's dotted path (like `shop.loaders.orders`), and loggers form a hierarchy by dots. Configuring `shop` configures everything beneath it, and you can quiet one noisy module without touching the others.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(name)s %(levelname)s %(message)s", force=True)

logging.getLogger("shop.loaders").info("visible")
logging.getLogger("shop.http").setLevel(logging.WARNING)
logging.getLogger("shop.http").info("hidden: this logger needs WARNING")
logging.getLogger("shop.http").warning("visible")
```

## Handlers and formatters

A **logger** creates records. A **handler** sends them somewhere (console, file, ...). A **formatter** decides the text. One logger can have several handlers at different levels.

```python
import io
import logging

stream = io.StringIO()
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s", datefmt="%H:%M:%S"))
handler.setLevel(logging.INFO)

log = logging.getLogger("demo.handlers")
log.setLevel(logging.DEBUG)
log.propagate = False            # do not also send to the root logger
log.addHandler(handler)

log.debug("dropped by the handler")
log.info("kept")
print(stream.getvalue().split("|", 1)[1].strip())
```

For files use `logging.FileHandler(path, encoding="utf-8")` or `RotatingFileHandler` so logs do not grow forever.

## Structured context

A message like `"failed"` is useless; `"load failed table=orders batch=42 rows=0"` is searchable. Put the identifying facts in the message as `key=value` pairs, or pass them through `extra=` so a formatter or JSON handler can emit them as fields.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s batch=%(batch)s", force=True)
log = logging.getLogger("etl.context")

log.info("loaded table=%s rows=%d", "orders", 1204, extra={"batch": 42})
```

Log **what**, **which**, **how many**. Never log secrets, whole records with personal data, or tokens (you saw `redact` earlier).

## Logging exceptions

Inside an `except` block, `log.exception("...")` logs at ERROR level and includes the traceback.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s", force=True)
log = logging.getLogger("etl.errors")

try:
    int("abc")
except ValueError:
    log.exception("could not parse amount for invoice=%s", "INV-7")
```

Then decide: swallow (the log is your record), or `raise` it onward. Do not both log and re-raise at every layer, or you get the same error five times. Log where you handle it.

## Testing logs

pytest's `caplog` fixture captures records so you can assert on them:

```python
# no-run   (this is a test, run it with pytest)
import logging

def test_warns_on_rejects(caplog):
    with caplog.at_level(logging.WARNING, logger="etl.load"):
        run_load(rows_with_bad_data)
    assert "rejected" in caplog.text
```

## Common mistakes

- Calling `logging.basicConfig()` inside a library, or after handlers already exist (it silently does nothing without `force=True`).
- f-strings in log calls, which format eagerly.
- Expecting INFO output without setting the level (default is WARNING).
- Duplicate lines: a handler added at both the logger and root level, or `addHandler` in a function called twice.
- Using `log.error(e)` and losing the traceback. Use `log.exception`.

## What to take away

1. `print` is output; `logging` is a record with severity, timestamp and a configurable destination.
2. `log = logging.getLogger(__name__)` in every module; libraries emit, applications configure.
3. Pass values as arguments: `log.info("rows=%d", n)`.
4. Loggers create, handlers deliver, formatters shape.
5. Include structured context; never secrets.
6. `log.exception` in `except` blocks; log once, where you handle.
