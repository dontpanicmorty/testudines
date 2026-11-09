from solution import parse_age


def test_valid():
    assert parse_age("34") == 34


def test_limits():
    assert parse_age("0") == 0
    assert parse_age("120") == 120
    assert parse_age("121") is None


def test_negative():
    assert parse_age("-5") is None


def test_not_a_number():
    assert parse_age("old") is None
    assert parse_age("") is None
    assert parse_age("12.5") is None


def test_spaces_around_digits_are_accepted():
    assert parse_age(" 40 ") == 40
