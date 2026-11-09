import logging

from solution import make_logger


def close(log):
    for h in list(log.handlers):
        h.close()
        log.removeHandler(h)


def test_format_and_level(tmp_path):
    p = tmp_path / "run.log"
    log = make_logger("t.run", p)
    try:
        log.debug("hidden")
        log.info("started")
        log.warning("slow")
        for h in log.handlers:
            h.flush()
        assert p.read_text(encoding="utf-8").splitlines() == ["INFO | t.run | started", "WARNING | t.run | slow"]
    finally:
        close(log)


def test_no_duplicate_handlers(tmp_path):
    p = tmp_path / "run.log"
    log = make_logger("t.dup", p)
    try:
        make_logger("t.dup", p)
        log.info("once")
        for h in log.handlers:
            h.flush()
        assert p.read_text(encoding="utf-8").splitlines() == ["INFO | t.dup | once"]
    finally:
        close(log)


def test_does_not_propagate(tmp_path, caplog):
    log = make_logger("t.prop", tmp_path / "x.log")
    try:
        with caplog.at_level(logging.INFO):
            log.info("hello")
        assert not [r for r in caplog.records if r.name == "t.prop"]
    finally:
        close(log)


def test_custom_level(tmp_path):
    p = tmp_path / "w.log"
    log = make_logger("t.lvl", p, level=logging.ERROR)
    try:
        log.warning("no")
        log.error("yes")
        for h in log.handlers:
            h.flush()
        assert p.read_text(encoding="utf-8").splitlines() == ["ERROR | t.lvl | yes"]
    finally:
        close(log)
