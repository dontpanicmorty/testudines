from solution import spread


def test_basic():
    assert spread([4, 9, 2]) == (2, 9)


def test_empty():
    assert spread([]) == (None, None)


def test_single():
    assert spread([5]) == (5, 5)


def test_negative_and_float():
    assert spread([-3, 2.5, 0]) == (-3, 2.5)


def test_returns_tuple():
    assert isinstance(spread([1, 2]), tuple)
