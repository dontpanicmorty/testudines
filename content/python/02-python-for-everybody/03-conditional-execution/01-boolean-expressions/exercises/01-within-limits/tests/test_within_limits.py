from solution import in_range


def test_inside():
    assert in_range(5, 1, 10) is True


def test_on_the_edges():
    assert in_range(1, 1, 10) is True
    assert in_range(10, 1, 10) is True


def test_outside():
    assert in_range(11, 1, 10) is False
    assert in_range(0, 1, 10) is False


def test_negative_range():
    assert in_range(-3, -5, -1) is True
