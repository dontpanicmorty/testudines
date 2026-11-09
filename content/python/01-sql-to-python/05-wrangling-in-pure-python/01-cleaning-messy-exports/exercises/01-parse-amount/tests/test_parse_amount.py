from decimal import Decimal

import pytest

from solution import parse_amount


def test_dollars_and_commas():
    assert parse_amount("$3,291.26") == Decimal("3291.26")
    assert type(parse_amount("$3,291.26")) is Decimal


def test_plain_and_spaces():
    assert parse_amount(" 1310.11 ") == Decimal("1310.11")


def test_missing_markers():
    for t in ["", "   ", "N/A", "n/a", " N/a "]:
        assert parse_amount(t) is None, repr(t)
    assert parse_amount(None) is None


def test_exact_not_float():
    assert parse_amount("0.10") + parse_amount("0.20") == Decimal("0.30")


def test_garbage_raises():
    with pytest.raises(ValueError):
        parse_amount("12 dollars")
