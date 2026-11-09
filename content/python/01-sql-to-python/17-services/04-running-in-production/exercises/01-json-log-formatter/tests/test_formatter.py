import io
import json
import logging
from datetime import date
from pathlib import Path

import pytest

from solution import JsonFormatter


@pytest.fixture
def logger_and_stream():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    log = logging.getLogger("access-test")
    log.handlers = [handler]
    log.setLevel(logging.DEBUG)
    log.propagate = False
    yield log, stream
    log.handlers = []


def last(stream):
    lines = stream.getvalue().splitlines()
    assert len(lines) == 1, f"expected one line, got {lines!r}"
    return json.loads(lines[0])


def test_basic_fields(logger_and_stream):
    log, stream = logger_and_stream
    log.info("hello")
    assert last(stream) == {"level": "INFO", "logger": "access-test", "message": "hello"}


def test_args_are_applied(logger_and_stream):
    log, stream = logger_and_stream
    log.warning("served %s in %d ms", "/orders", 12)
    out = last(stream)
    assert out["message"] == "served /orders in 12 ms" and out["level"] == "WARNING"


def test_extra_fields_merged_top_level(logger_and_stream):
    log, stream = logger_and_stream
    log.info("req", extra={"fields": {"status": 200, "ms": 12.5}})
    out = last(stream)
    assert out["status"] == 200 and out["ms"] == 12.5


def test_no_exc_key_without_exception(logger_and_stream):
    log, stream = logger_and_stream
    log.info("fine")
    assert "exc" not in last(stream)


def test_exception_included_single_line_json(logger_and_stream):
    log, stream = logger_and_stream
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("failed")
    out = last(stream)
    assert "ZeroDivisionError" in out["exc"]
    assert out["level"] == "ERROR"


def test_non_serialisable_values_become_strings(logger_and_stream):
    log, stream = logger_and_stream
    log.info("x", extra={"fields": {"day": date(2025, 1, 2), "path": Path("/tmp/a")}})
    out = last(stream)
    assert out["day"] == "2025-01-02" and out["path"] == str(Path("/tmp/a"))  # "\\tmp\\a" on Windows


def test_newlines_in_message_stay_one_line(logger_and_stream):
    log, stream = logger_and_stream
    log.info("a\nb")
    assert last(stream)["message"] == "a\nb"
