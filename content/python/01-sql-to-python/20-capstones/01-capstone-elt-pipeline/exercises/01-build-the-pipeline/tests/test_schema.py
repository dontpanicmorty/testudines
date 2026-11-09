import pytest

from pipeline.schema import validate_customers, validate_items, validate_orders

GOOD = {"order_id": "7", "customer_id": " 3 ", "placed_at": "2025-03-04 05:06:07", "status": " Shipped "}


def test_good_order_is_typed_and_normalised():
    good, bad = validate_orders([GOOD])
    assert bad == []
    assert good == [{"order_id": 7, "customer_id": 3, "placed_at": "2025-03-04 05:06:07", "status": "shipped"}]


@pytest.mark.parametrize("field,value", [
    ("order_id", "abc"), ("order_id", "0"), ("order_id", ""),
    ("customer_id", "-4"), ("customer_id", "x"),
    ("placed_at", "2025-13-45 00:00:00"), ("placed_at", "04/03/2025"), ("placed_at", ""),
    ("status", "teleported"), ("status", ""),
])
def test_bad_order_is_quarantined_with_field_in_reason(field, value):
    row = dict(GOOD, **{field: value})
    good, bad = validate_orders([row])
    assert good == []
    assert len(bad) == 1
    assert bad[0]["source"] == "orders"
    assert bad[0]["raw"] == row
    assert field in bad[0]["reason"], bad[0]["reason"]


def test_missing_key_is_quarantined_not_crash():
    row = {"order_id": "1", "customer_id": "1", "status": "completed"}   # no placed_at
    good, bad = validate_orders([row])
    assert good == [] and len(bad) == 1


def test_duplicate_order_id_first_wins():
    first = dict(GOOD)
    second = dict(GOOD, status="refunded")
    good, bad = validate_orders([first, second])
    assert len(good) == 1 and good[0]["status"] == "shipped"
    assert len(bad) == 1 and "duplicate" in bad[0]["reason"]


def test_good_and_bad_are_split_and_order_preserved():
    rows = [dict(GOOD, order_id="1"), dict(GOOD, order_id="x"), dict(GOOD, order_id="3")]
    good, bad = validate_orders(rows)
    assert [g["order_id"] for g in good] == [1, 3]
    assert len(bad) == 1


def test_input_rows_not_mutated():
    row = dict(GOOD)
    validate_orders([row])
    assert row == GOOD


def test_items_valid_and_invalid():
    rows = [
        {"order_id": "1", "product_id": " P1 ", "quantity": "2", "unit_price": "10.50"},
        {"order_id": "1", "product_id": "P2", "quantity": "0", "unit_price": "1"},
        {"order_id": "1", "product_id": "P2", "quantity": "1", "unit_price": "abc"},
        {"order_id": "1", "product_id": "P2", "quantity": "1", "unit_price": "-1"},
        {"order_id": "1", "product_id": "", "quantity": "1", "unit_price": "1"},
        {"order_id": "z", "product_id": "P2", "quantity": "1", "unit_price": "1"},
    ]
    good, bad = validate_items(rows)
    assert good == [{"order_id": 1, "product_id": "P1", "quantity": 2, "unit_price": 10.5}]
    assert len(bad) == 5
    assert all(b["source"] == "order_items" for b in bad)
    reasons = " ".join(b["reason"] for b in bad)
    for word in ("quantity", "unit_price", "product_id", "order_id"):
        assert word in reasons


def test_same_product_twice_on_an_order_is_allowed():
    rows = [{"order_id": "1", "product_id": "P1", "quantity": "1", "unit_price": "1"}] * 2
    good, bad = validate_items(rows)
    assert len(good) == 2 and bad == []


def test_customers():
    rows = [
        {"customer_id": "1", "region": " West "},
        {"customer_id": "1", "region": "east"},
        {"customer_id": "2", "region": ""},
        {"customer_id": "abc", "region": "east"},
    ]
    good, bad = validate_customers(rows)
    assert good == [{"customer_id": 1, "region": "west"}]
    assert len(bad) == 3 and all(b["source"] == "customers" for b in bad)
