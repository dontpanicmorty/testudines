from decimal import Decimal

from solution import group_totals


def test_basic_and_none():
    rows = [{"region": "EU", "amt": 50}, {"region": "US", "amt": 20}, {"region": "EU", "amt": None}]
    assert group_totals(rows, "region", "amt") == {
        "EU": {"count": 2, "total": 50},
        "US": {"count": 1, "total": 20},
    }


def test_empty():
    assert group_totals([], "k", "v") == {}


def test_decimals():
    rows = [{"k": "a", "v": Decimal("0.10")}, {"k": "a", "v": Decimal("0.20")}]
    assert group_totals(rows, "k", "v")["a"]["total"] == Decimal("0.30")


def test_key_column_is_generic():
    rows = [{"plan": "pro", "n": 1}, {"plan": "pro", "n": 2}]
    assert group_totals(rows, "plan", "n") == {"pro": {"count": 2, "total": 3}}
