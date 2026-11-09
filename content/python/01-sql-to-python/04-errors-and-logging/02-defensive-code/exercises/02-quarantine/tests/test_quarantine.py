import pytest

from solution import TooManyRejects, process


def positive(x):
    if x <= 0:
        raise ValueError(f"not positive: {x}")
    return x * 10


def test_split():
    rows = list(range(1, 100)) + [-1]
    good, rejected = process(rows, positive, max_reject_rate=0.05)
    assert good == [x * 10 for x in range(1, 100)]
    assert rejected == [{"row": 100, "reason": "not positive: -1", "raw": -1}]


def test_threshold_is_strictly_greater():
    rows = [1, 1, 1, -1]
    good, rejected = process(rows, positive, max_reject_rate=0.25)
    assert len(rejected) == 1


def test_too_many():
    with pytest.raises(TooManyRejects):
        process([1, -1, -2, 3], positive, max_reject_rate=0.25)


def test_empty():
    assert process([], positive) == ([], [])


def test_other_errors_propagate():
    def boom(x):
        raise KeyError("bug")

    with pytest.raises(KeyError):
        process([1], boom)
