from solution import more_than_double


def test_true():
    assert more_than_double(10, 3) is True


def test_exactly_two():
    assert more_than_double(10, 5) is False


def test_zero_divisor():
    assert more_than_double(10, 0) is False


def test_negative_divisor():
    assert more_than_double(10, -2) is False
