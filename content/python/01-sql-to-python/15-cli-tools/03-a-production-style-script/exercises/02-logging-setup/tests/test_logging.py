import io
import logging

from solution import setup_logging


def test_format_and_level():
    buf = io.StringIO()
    log = setup_logging(stream=buf)
    log.debug("hidden")
    log.info("loaded %d rows", 3)
    log.warning("careful")
    assert buf.getvalue() == "INFO jobrunner: loaded 3 rows\nWARNING jobrunner: careful\n"


def test_verbose_shows_debug():
    buf = io.StringIO()
    setup_logging(verbose=True, stream=buf).debug("x=%d", 1)
    assert buf.getvalue() == "DEBUG jobrunner: x=1\n"


def test_repeat_calls_do_not_duplicate():
    a, b = io.StringIO(), io.StringIO()
    setup_logging(stream=a)
    log = setup_logging(stream=b)
    log.info("once")
    assert a.getvalue() == "", "old handler should have been replaced"
    assert b.getvalue() == "INFO jobrunner: once\n"
    assert len(log.handlers) == 1


def test_returns_named_logger_without_propagation():
    log = setup_logging(stream=io.StringIO())
    assert log is logging.getLogger("jobrunner")
    assert log.propagate is False


def test_defaults_to_stderr(capsys):
    setup_logging().info("to stderr")
    out = capsys.readouterr()
    assert out.out == "" and "INFO jobrunner: to stderr" in out.err
