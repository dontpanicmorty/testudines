from solution import to_whole_number


def test_valid():
    assert to_whole_number("42", 0) == 42


def test_invalid_text():
    assert to_whole_number("abc", -1) == -1


def test_decimal_text_is_not_whole():
    assert to_whole_number("3.5", 0) == 0


def test_empty_and_negative():
    assert to_whole_number("", 7) == 7
    assert to_whole_number("-8", 0) == -8
