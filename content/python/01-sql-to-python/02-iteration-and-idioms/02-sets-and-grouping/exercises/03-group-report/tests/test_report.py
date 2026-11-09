from solution import revenue_report


def test_basic():
    orders = [
        {"region": "EU", "plan": "pro", "amount": 10.0},
        {"region": "EU", "plan": "pro", "amount": 5.0},
        {"region": "US", "plan": "free", "amount": 1.0},
    ]
    assert revenue_report(orders) == [
        {"region": "EU", "plan": "pro", "orders": 2, "revenue": 15.0, "avg": 7.5},
        {"region": "US", "plan": "free", "orders": 1, "revenue": 1.0, "avg": 1.0},
    ]


def test_sorted_and_rounded():
    orders = [
        {"region": "US", "plan": "b", "amount": 0.1},
        {"region": "EU", "plan": "z", "amount": 1.0},
        {"region": "EU", "plan": "a", "amount": 0.1},
        {"region": "EU", "plan": "a", "amount": 0.2},
        {"region": "EU", "plan": "a", "amount": 0.2},
    ]
    out = revenue_report(orders)
    assert [(r["region"], r["plan"]) for r in out] == [("EU", "a"), ("EU", "z"), ("US", "b")]
    assert out[0]["revenue"] == 0.5 and out[0]["avg"] == 0.17


def test_empty():
    assert revenue_report([]) == []
