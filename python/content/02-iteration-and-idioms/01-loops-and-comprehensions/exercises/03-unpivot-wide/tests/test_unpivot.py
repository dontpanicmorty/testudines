from solution import unpivot


def test_basic():
    rows = [{"product": "A", "2024-01": "10.5", "2024-02": None},
            {"product": "B", "2024-01": "3", "2024-02": "4.25"}]
    assert unpivot(rows) == [
        {"product": "A", "month": "2024-01", "revenue": 10.5},
        {"product": "B", "month": "2024-01", "revenue": 3.0},
        {"product": "B", "month": "2024-02", "revenue": 4.25},
    ]


def test_blank_strings_skipped():
    assert unpivot([{"product": "A", "m1": "", "m2": "1"}]) == [{"product": "A", "month": "m2", "revenue": 1.0}]


def test_custom_id_field():
    out = unpivot([{"sku": "S", "m1": "2"}], id_field="sku")
    assert out == [{"sku": "S", "month": "m1", "revenue": 2.0}]


def test_empty():
    assert unpivot([]) == []
