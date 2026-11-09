from solution import numbers_in


def test_basic():
    assert numbers_in("Rooms 12, 7 and 130") == [12, 7, 130]


def test_none():
    assert numbers_in("no digits here") == []


def test_empty():
    assert numbers_in("") == []


def test_decimal_splits():
    assert numbers_in("3.5") == [3, 5]


def test_glued_to_letters():
    assert numbers_in("a1b22c") == [1, 22]


def test_leading_zeros():
    assert numbers_in("007") == [7]
