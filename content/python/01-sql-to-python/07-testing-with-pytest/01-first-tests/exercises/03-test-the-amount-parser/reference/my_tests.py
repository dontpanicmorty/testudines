import pytest

from amounts import parse_amount


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("42", 42.0),
        ("$42", 42.0),
        (" 1,234.50 ", 1234.5),
        ("$1,234,567.89", 1234567.89),
        ("(12.00)", -12.0),
        ("($1,000.00)", -1000.0),
    ],
)
def test_numbers(raw, expected):
    assert parse_amount(raw) == pytest.approx(expected)


@pytest.mark.parametrize("raw", [None, "", "   ", "N/A", "n/a", "N/a"])
def test_missing_values_are_none(raw):
    assert parse_amount(raw) is None


@pytest.mark.parametrize("raw", ["abc", "12abc", "$$"])
def test_garbage_raises(raw):
    with pytest.raises(ValueError):
        parse_amount(raw)
