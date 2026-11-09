import pytest

from solution import retry


def make_flaky(failures, exc=TimeoutError("slow")):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise exc
        return "ok"

    return fn, state


def transient(e):
    return isinstance(e, TimeoutError)


def test_success_first_try():
    fn, state = make_flaky(0)
    waits = []
    assert retry(fn, 3, transient, sleep=waits.append) == "ok"
    assert state["calls"] == 1 and waits == []


def test_backoff_delays():
    fn, state = make_flaky(2)
    waits = []
    assert retry(fn, 4, transient, base_delay=0.5, sleep=waits.append) == "ok"
    assert waits == [0.5, 1.0]
    assert state["calls"] == 3


def test_gives_up_and_raises_last_error():
    fn, state = make_flaky(10)
    waits = []
    with pytest.raises(TimeoutError, match="slow"):
        retry(fn, 3, transient, base_delay=1, sleep=waits.append)
    assert state["calls"] == 3
    assert waits == [1, 2], "no sleep after the final attempt"


def test_permanent_error_not_retried():
    fn, state = make_flaky(5, exc=ValueError("bad"))
    waits = []
    with pytest.raises(ValueError):
        retry(fn, 5, transient, sleep=waits.append)
    assert state["calls"] == 1 and waits == []
