from solution import mean


def test_basic():
    assert mean([2, 4, 9]) == 5.0


def test_empty():
    assert mean([]) is None


def test_negative():
    assert mean([-1, 1]) == 0


def test_fraction():
    assert mean([1, 2]) == 1.5
