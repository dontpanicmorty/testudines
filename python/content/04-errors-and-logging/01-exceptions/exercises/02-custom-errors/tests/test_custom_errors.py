import pytest

from solution import RowError, parse_row


def test_ok():
    assert parse_row({"id": "7", "amount": "12.5"}, 1) == {"id": 7, "amount": 12.5}


def test_bad_amount_message_and_cause():
    with pytest.raises(RowError) as exc:
        parse_row({"id": "7", "amount": "abc"}, 3)
    assert "row 3" in str(exc.value)
    assert "abc" in str(exc.value)
    assert exc.value.row_number == 3
    assert isinstance(exc.value.__cause__, ValueError)


def test_bad_id():
    with pytest.raises(RowError) as exc:
        parse_row({"id": "x", "amount": "1"}, 9)
    assert exc.value.row_number == 9


def test_missing_key_not_wrapped():
    with pytest.raises(KeyError):
        parse_row({"id": "7"}, 1)


def test_is_exception():
    assert issubclass(RowError, Exception)
