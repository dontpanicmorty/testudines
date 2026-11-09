from solution import first_integer


def test_negative():
    assert first_integer("temp is -12 today") == -12


def test_first_of_many():
    assert first_integer("room 7 and 9") == 7


def test_none():
    assert first_integer("nothing") is None


def test_empty():
    assert first_integer("") is None


def test_returns_int():
    assert isinstance(first_integer("a1"), int)


def test_dash_without_digits_ignored():
    assert first_integer("a - b 5") == 5
