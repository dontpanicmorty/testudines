from solution import priciest


def test_basic():
    assert priciest({"tea": 3, "milk": 2, "rice": 5}) == ("rice", 5)


def test_empty():
    assert priciest({}) is None


def test_tie_alphabetical():
    assert priciest({"b": 4, "a": 4, "c": 1}) == ("a", 4)


def test_single():
    assert priciest({"x": 0}) == ("x", 0)


def test_negative_prices():
    assert priciest({"a": -5, "b": -2}) == ("b", -2)
