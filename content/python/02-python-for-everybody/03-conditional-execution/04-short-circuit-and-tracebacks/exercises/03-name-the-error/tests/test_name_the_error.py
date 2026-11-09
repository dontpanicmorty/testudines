from solution import error_name


def test_zero_division():
    assert error_name(lambda: 10 / 0) == "ZeroDivisionError"


def test_value_error():
    assert error_name(lambda: int("abc")) == "ValueError"


def test_no_error():
    assert error_name(lambda: 1 + 1) == "none"


def test_type_error():
    assert error_name(lambda: "a" + 1) == "TypeError"


def test_index_error():
    assert error_name(lambda: "abc"[10]) == "IndexError"
