import pytest

from solution import evaluate


def test_within_budget():
    assert evaluate(100, 5, 0.1) == (0, "ok: 5 of 100 rows rejected")


def test_exactly_at_budget_is_ok():
    assert evaluate(100, 10, 0.1)[0] == 0


def test_over_budget():
    assert evaluate(100, 20, 0.1) == (1, "error rate 20.0% exceeds budget of 10.0%")


def test_empty_input():
    assert evaluate(0, 0, 0.5) == (1, "no input rows")


def test_zero_tolerance():
    assert evaluate(10, 0, 0.0)[0] == 0
    assert evaluate(10, 1, 0.0)[0] == 1


@pytest.mark.parametrize("args", [(10, 11, 0.1), (10, -1, 0.1), (10, 1, 1.5), (10, 1, -0.1)])
def test_invalid_inputs(args):
    with pytest.raises(ValueError):
        evaluate(*args)
