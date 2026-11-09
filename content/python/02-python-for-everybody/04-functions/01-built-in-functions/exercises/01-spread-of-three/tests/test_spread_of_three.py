from solution import spread


def test_basic():
    assert spread(4, 19, 7) == 15


def test_all_equal():
    assert spread(5, 5, 5) == 0


def test_negatives():
    assert spread(-3, 4, 0) == 7


def test_decimals():
    assert abs(spread(0.5, 2.25, 1) - 1.75) < 1e-9
