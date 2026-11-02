from solution import error_report

REJECTS = [
    {"index": 1, "row": {}, "errors": [{"field": "amount", "message": "m"}]},
    {"index": 4, "row": {}, "errors": [{"field": "amount", "message": "m"}, {"field": "status", "message": "m"}]},
    {"index": 9, "row": {}, "errors": [{"field": "status", "message": "m"}, {"field": "status", "message": "n"}]},
    {"index": 12, "row": {}, "errors": [{"field": "id", "message": "m"}]},
]


def test_report():
    r = error_report(REJECTS, 40)
    assert r["rejected"] == 4
    assert r["reject_rate"] == 0.1
    assert r["by_field"] == [
        {"field": "status", "error_count": 3, "rows_affected": 2},
        {"field": "amount", "error_count": 2, "rows_affected": 2},
        {"field": "id", "error_count": 1, "rows_affected": 1},
    ], r["by_field"]
    assert r["sample_indexes"] == [1, 4, 9]


def test_empty_and_zero_total():
    assert error_report([], 10) == {"rejected": 0, "reject_rate": 0.0, "by_field": [], "sample_indexes": []}
    assert error_report([], 0)["reject_rate"] == 0.0


def test_rounding():
    r = error_report(REJECTS[:1], 3)
    assert r["reject_rate"] == 0.3333
