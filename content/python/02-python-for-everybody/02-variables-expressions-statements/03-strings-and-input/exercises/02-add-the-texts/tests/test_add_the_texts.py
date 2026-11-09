from solution import add_texts


def test_whole():
    assert add_texts("3", "4") == 7


def test_decimals():
    assert add_texts("2.5", "0.25") == 2.75


def test_negative():
    assert add_texts("-1", "1") == 0


def test_returns_number():
    assert not isinstance(add_texts("1", "1"), str)
