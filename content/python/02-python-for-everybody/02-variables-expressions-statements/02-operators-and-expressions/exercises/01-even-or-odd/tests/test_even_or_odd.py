from solution import is_even


def test_even():
    assert is_even(10) is True


def test_odd():
    assert is_even(7) is False


def test_zero():
    assert is_even(0) is True


def test_negative_odd():
    assert is_even(-3) is False
