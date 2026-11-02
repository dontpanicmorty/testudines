import functools

import pytest

from datakit import retry


class Flaky:
    def __init__(self, failures, exc=ConnectionError):
        self.failures, self.exc, self.calls = failures, exc, 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.exc(f"fail {self.calls}")
        return ("ok", args, kwargs)


def test_success_first_try_no_sleep():
    sleeps = []
    f = retry(attempts=3, sleep=sleeps.append)(Flaky(0))
    assert f(1, a=2) == ("ok", (1,), {"a": 2})
    assert sleeps == []


def test_retries_then_succeeds():
    flaky = Flaky(2)
    sleeps = []
    f = retry(attempts=3, delay=1.0, backoff=2.0, sleep=sleeps.append)(flaky)
    assert f()[0] == "ok"
    assert flaky.calls == 3
    assert sleeps == [1.0, 2.0]


def test_exhaustion_reraises_original_exception():
    flaky = Flaky(10)
    f = retry(attempts=3, sleep=lambda s: None)(flaky)
    with pytest.raises(ConnectionError) as exc:
        f()
    assert str(exc.value) == "fail 3"
    assert flaky.calls == 3


def test_no_sleep_after_last_attempt():
    sleeps = []
    f = retry(attempts=3, delay=1.0, sleep=sleeps.append)(Flaky(10))
    with pytest.raises(ConnectionError):
        f()
    assert len(sleeps) == 2


def test_only_listed_exceptions_are_retried():
    flaky = Flaky(5, exc=KeyError)
    f = retry(attempts=5, exceptions=(ConnectionError,), sleep=lambda s: None)(flaky)
    with pytest.raises(KeyError):
        f()
    assert flaky.calls == 1


def test_tuple_of_exceptions():
    flaky = Flaky(1, exc=TimeoutError)
    f = retry(attempts=2, exceptions=(ConnectionError, TimeoutError), sleep=lambda s: None)(flaky)
    assert f()[0] == "ok"


def test_default_backoff_doubles():
    sleeps = []
    f = retry(attempts=4, delay=0.5, sleep=sleeps.append)(Flaky(3))
    f()
    assert sleeps == [0.5, 1.0, 2.0]


def test_zero_delay_default_sleeps_zero():
    sleeps = []
    retry(attempts=2, sleep=sleeps.append)(Flaky(1))()
    assert sleeps == [0.0]


def test_preserves_metadata():
    @retry(attempts=2)
    def load_orders(path: str) -> int:
        """Load orders."""
        return 1

    assert load_orders.__name__ == "load_orders"
    assert load_orders.__doc__ == "Load orders."


def test_works_as_decorator_on_methods():
    class Client:
        def __init__(self):
            self.n = 0

        @retry(attempts=3, sleep=lambda s: None)
        def get(self):
            self.n += 1
            if self.n < 3:
                raise ConnectionError
            return self.n

    assert Client().get() == 3


def test_each_call_gets_fresh_attempt_budget():
    flaky = Flaky(1)
    f = retry(attempts=2, sleep=lambda s: None)(flaky)
    f()
    flaky.calls = 0
    assert f()[0] == "ok"


@pytest.mark.parametrize("kwargs", [{"attempts": 0}, {"delay": -1}, {"backoff": 0.5}])
def test_invalid_arguments(kwargs):
    with pytest.raises(ValueError):
        retry(**kwargs)


def test_attempts_one_means_no_retry():
    flaky = Flaky(1)
    with pytest.raises(ConnectionError):
        retry(attempts=1, sleep=lambda s: None)(flaky)()
    assert flaky.calls == 1
