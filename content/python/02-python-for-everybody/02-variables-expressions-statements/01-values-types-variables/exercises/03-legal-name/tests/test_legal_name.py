from solution import can_be_variable_name


def test_good_name():
    assert can_be_variable_name("cups_of_tea") is True
    assert can_be_variable_name("_hidden") is True


def test_starts_with_digit():
    assert can_be_variable_name("2cups") is False


def test_space_and_hyphen():
    assert can_be_variable_name("my tea") is False
    assert can_be_variable_name("my-tea") is False


def test_reserved_word():
    assert can_be_variable_name("while") is False
    assert can_be_variable_name("None") is False


def test_empty():
    assert can_be_variable_name("") is False
