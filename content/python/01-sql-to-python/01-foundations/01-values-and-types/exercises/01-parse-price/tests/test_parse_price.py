from solution import parse_price


def test_dollar_and_commas():
    assert parse_price("$1,234.50") == 1234.5


def test_whitespace_no_symbol():
    assert parse_price("  99.00 ") == 99.0


def test_returns_float():
    assert isinstance(parse_price("5"), float)
