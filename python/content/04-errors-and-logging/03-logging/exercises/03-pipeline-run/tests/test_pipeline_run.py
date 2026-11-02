import logging

import pytest

from solution import run_step


def msgs(caplog):
    return [(r.levelname, r.getMessage()) for r in caplog.records if r.name == "solution"]


def test_mixed(caplog):
    with caplog.at_level(logging.INFO):
        out = run_step(["1", "x", "3"], int, "r1")
    assert out == [1, 3]
    m = msgs(caplog)
    assert m[0][0] == "WARNING"
    assert m[0][1].startswith("run=r1 row=2 skipped:")
    assert m[1] == ("INFO", "run=r1 ok=2 skipped=1")
    assert len(m) == 2


def test_clean_run(caplog):
    with caplog.at_level(logging.INFO):
        assert run_step(["1", "2"], int, "r2") == [1, 2]
    assert msgs(caplog) == [("INFO", "run=r2 ok=2 skipped=0")]


def test_too_many(caplog):
    with caplog.at_level(logging.INFO):
        with pytest.raises(RuntimeError):
            run_step(["a", "b", "c", "4"], int, "r3", max_failures=2)
    m = msgs(caplog)
    assert m[-1] == ("ERROR", "run=r3 too many failures skipped=3")
    assert not any(level == "INFO" for level, _ in m)


def test_other_errors_propagate():
    def boom(_):
        raise KeyError("bug")

    with pytest.raises(KeyError):
        run_step([1], boom, "r4")
