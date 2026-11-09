from solution import kind_of


def test_int():
    assert kind_of(7) == "int"


def test_str_digits():
    assert kind_of("7") == "str"


def test_float():
    assert kind_of(7.0) == "float"


def test_empty_text():
    assert kind_of("") == "str"
