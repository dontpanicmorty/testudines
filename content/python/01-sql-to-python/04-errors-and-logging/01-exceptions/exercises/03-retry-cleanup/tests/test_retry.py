import pytest

from solution import load_with_retry


class Counter:
    def __init__(self):
        self.closed = 0

    def close(self):
        self.closed += 1


def test_success_first_try():
    c = Counter()
    assert load_with_retry(lambda: "ok", 3, c.close) == "ok"
    assert c.closed == 1


def test_retries_then_succeeds():
    c = Counter()
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionError("down")
        return "ok"

    assert load_with_retry(flaky, 5, c.close) == "ok"
    assert len(calls) == 3
    assert c.closed == 1


def test_gives_up_with_cause():
    c = Counter()

    def always():
        raise ConnectionError("down")

    with pytest.raises(ConnectionError) as exc:
        load_with_retry(always, 2, c.close)
    assert "giving up after 2 attempts" in str(exc.value)
    assert isinstance(exc.value.__cause__, ConnectionError)
    assert c.closed == 1


def test_other_errors_not_retried():
    c = Counter()
    calls = []

    def buggy():
        calls.append(1)
        raise TypeError("bug")

    with pytest.raises(TypeError):
        load_with_retry(buggy, 5, c.close)
    assert len(calls) == 1
    assert c.closed == 1
