import pytest

from solution import best_of


class FakeClock:
    """Each read returns the next value in the list."""

    def __init__(self, values):
        self.values = list(values)

    def __call__(self):
        return self.values.pop(0)


def test_returns_min_run_per_call():
    clock = FakeClock([0, 10, 10, 14, 14, 30])   # runs: 10, 4, 16
    assert best_of(lambda: None, number=2, repeat=3, timer=clock) == 2.0


def test_calls_fn_number_times_per_run():
    calls = []
    clock = FakeClock([0, 1, 1, 2])
    best_of(lambda: calls.append(1), number=7, repeat=2, timer=clock)
    assert len(calls) == 14


def test_timer_read_exactly_twice_per_run():
    clock = FakeClock([0, 1, 1, 2, 2, 3])
    best_of(lambda: None, number=1, repeat=3, timer=clock)
    assert clock.values == []


def test_default_timer_real_clock():
    t = best_of(lambda: sum(range(100)), number=50, repeat=2)
    assert isinstance(t, float) and 0 <= t < 0.1


@pytest.mark.parametrize("kw", [{"number": 0}, {"repeat": 0}])
def test_invalid_args(kw):
    with pytest.raises(ValueError):
        best_of(lambda: None, **kw)
