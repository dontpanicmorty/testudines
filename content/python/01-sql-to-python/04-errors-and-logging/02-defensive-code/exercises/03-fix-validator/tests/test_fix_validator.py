import pytest

from solution import clean_orders


def row(order_id="A", quantity="2", status="Paid"):
    return {"order_id": order_id, "quantity": quantity, "status": status}


def test_clean():
    assert clean_orders([row()]) == [{"order_id": "A", "quantity": 2, "status": "paid"}]


def test_dedupe_first_wins():
    out = clean_orders([row("A", "1"), row("A", "9"), row("B")])
    assert [(o["order_id"], o["quantity"]) for o in out] == [("A", 1), ("B", 2)]


def test_no_state_between_calls():
    clean_orders([row("A")])
    assert len(clean_orders([row("A")])) == 1


def test_bad_values_raise_value_error():
    for bad in (row(order_id=""), row(quantity="0"), row(status="refunded"), row(status=None)):
        with pytest.raises(ValueError) as exc:
            clean_orders([bad])
        assert not isinstance(exc.value, AssertionError)


def test_non_numeric_quantity():
    with pytest.raises(ValueError):
        clean_orders([row(quantity="two")])


def test_caller_supplied_seen_ids_not_mutated():
    seen = {"A"}
    out = clean_orders([row("A"), row("B")], seen_ids=seen)
    assert [o["order_id"] for o in out] == ["B"]
    assert seen == {"A"}
