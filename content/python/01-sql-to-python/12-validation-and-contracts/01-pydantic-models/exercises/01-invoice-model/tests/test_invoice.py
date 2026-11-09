import pytest
from pydantic import ValidationError
from solution import Invoice, parse_invoice

GOOD = {"invoice_id": "INV-1", "customer": "Ada", "amount": "12.50", "status": "paid"}


def test_good_row_converted():
    inv = parse_invoice(GOOD)
    assert isinstance(inv, Invoice)
    assert inv.amount == 12.5 and isinstance(inv.amount, float)
    assert inv.invoice_id == "INV-1" and inv.status == "paid"


def test_extra_keys_ignored():
    assert parse_invoice({**GOOD, "note": "hello"}).customer == "Ada"


@pytest.mark.parametrize("patch", [
    {"amount": "-1"}, {"amount": "abc"}, {"status": "refunded"},
])
def test_bad_values_raise(patch):
    with pytest.raises(ValidationError):
        parse_invoice({**GOOD, **patch})


def test_missing_field_raises():
    row = dict(GOOD)
    del row["customer"]
    with pytest.raises(ValidationError):
        parse_invoice(row)


def test_zero_is_allowed():
    assert parse_invoice({**GOOD, "amount": "0"}).amount == 0.0
