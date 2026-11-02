from solution import try_int


def test_ok():
    assert try_int(" 42 ") == 42
    assert try_int("-7") == -7


def test_bad_text():
    assert try_int("abc") is None
    assert try_int("3.5", -1) == -1
    assert try_int("") is None


def test_none():
    assert try_int(None) is None
    assert try_int(None, 5) == 5
