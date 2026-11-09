from solution import bookends


def test_basic():
    assert bookends("python") == "pn"


def test_single_character():
    assert bookends("x") == "xx"


def test_empty():
    assert bookends("") == ""


def test_with_space():
    assert bookends("a b") == "ab"
