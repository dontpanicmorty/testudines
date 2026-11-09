from decimal import Decimal

from solution import customer_totals


def line(c, q, p):
    return {"customer_id": c, "quantity": q, "unit_price": Decimal(p), "sku": "X"}


def test_example():
    out = customer_totals([line(2, 3, "12.50"), line(1, 2, "5.00")])
    assert out == [
        {"customer_id": 1, "line_count": 1, "revenue": Decimal("10.00")},
        {"customer_id": 2, "line_count": 1, "revenue": Decimal("37.50")},
    ]


def test_accumulates():
    out = customer_totals([line(1, 1, "0.10"), line(1, 1, "0.20"), line(1, 3, "1.00")])
    assert out == [{"customer_id": 1, "line_count": 3, "revenue": Decimal("3.30")}]


def test_empty():
    assert customer_totals([]) == []
