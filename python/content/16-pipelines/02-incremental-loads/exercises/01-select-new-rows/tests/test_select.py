from solution import select_new

ROWS = [
    {"id": 3, "updated_at": "2026-01-02T08:00:00"},
    {"id": 1, "updated_at": "2026-01-01T09:00:00"},
    {"id": 2, "updated_at": "2026-01-01T10:00:00"},
]


def test_first_run_takes_everything_sorted():
    new, mark = select_new(ROWS, None)
    assert [r["id"] for r in new] == [1, 2, 3]
    assert mark == "2026-01-02T08:00:00"


def test_strictly_greater():
    new, mark = select_new(ROWS, "2026-01-01T10:00:00")
    assert [r["id"] for r in new] == [3]
    assert mark == "2026-01-02T08:00:00"


def test_nothing_new_keeps_watermark():
    new, mark = select_new(ROWS, "2026-01-02T08:00:00")
    assert new == []
    assert mark == "2026-01-02T08:00:00"


def test_empty_source_first_run():
    assert select_new([], None) == ([], None)
