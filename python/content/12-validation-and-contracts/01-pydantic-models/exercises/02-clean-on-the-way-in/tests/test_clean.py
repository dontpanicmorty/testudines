import pytest
from pydantic import ValidationError
from solution import parse_clean


def test_messy_row():
    c = parse_clean({"invoice_id": " INV-9 ", "customer": "  margaret LISKOV ",
                     "amount": "$3,291.26", "status": "PAID "})
    assert (c.invoice_id, c.customer, c.amount, c.status) == ("INV-9", "Margaret Liskov", 3291.26, "paid")


@pytest.mark.parametrize("raw", ["", "N/A", None, "  "])
def test_missing_amounts(raw):
    assert parse_clean({"invoice_id": "1", "customer": "a", "amount": raw}).amount is None


def test_status_defaults():
    assert parse_clean({"invoice_id": "1", "customer": "a"}).status == "unknown"
    assert parse_clean({"invoice_id": "1", "customer": "a", "status": ""}).status == "unknown"
    assert parse_clean({"invoice_id": "1", "customer": "a", "status": None}).status == "unknown"


def test_plain_number_amount():
    assert parse_clean({"invoice_id": "1", "customer": "a", "amount": 5}).amount == 5.0


@pytest.mark.parametrize("patch", [{"amount": "abc"}, {"status": "lost"}])
def test_garbage_raises(patch):
    with pytest.raises(ValidationError):
        parse_clean({"invoice_id": "1", "customer": "a", **patch})
