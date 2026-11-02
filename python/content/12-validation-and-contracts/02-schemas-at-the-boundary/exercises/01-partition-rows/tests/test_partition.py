import json
from pydantic import BaseModel
from solution import partition


class Order(BaseModel):
    order_id: int
    amount: float


ROWS = [
    {"order_id": "1", "amount": "9.5"},
    {"order_id": "x"},
    {"order_id": "3", "amount": "7"},
    {"order_id": "4", "amount": "bad"},
]


def test_valid_in_order():
    valid, _ = partition(ROWS, Order)
    assert [o.order_id for o in valid] == [1, 3]
    assert isinstance(valid[0], Order)


def test_reject_shape():
    _, rejects = partition(ROWS, Order)
    assert [r["index"] for r in rejects] == [1, 3]
    assert rejects[0]["row"] is ROWS[1]
    fields = sorted(e["field"] for e in rejects[0]["errors"])
    assert fields == ["amount", "order_id"], "all errors of the row should be reported"
    assert [e["field"] for e in rejects[1]["errors"]] == ["amount"]


def test_errors_are_plain_and_json_safe():
    _, rejects = partition(ROWS, Order)
    json.dumps(rejects)
    assert all(isinstance(e["message"], str) for r in rejects for e in r["errors"])


def test_empty_and_all_good():
    assert partition([], Order) == ([], [])
    valid, rejects = partition([{"order_id": 1, "amount": 2}], Order)
    assert len(valid) == 1 and rejects == []
