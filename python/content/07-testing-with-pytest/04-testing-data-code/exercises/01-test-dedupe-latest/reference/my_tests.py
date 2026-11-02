import copy

from dedupe import dedupe_latest


def row(id_, ts, v=""):
    return {"id": id_, "updated_at": ts, "v": v}


def test_latest_timestamp_wins_even_when_not_last_or_first():
    rows = [row(1, "2025-01-02", "mid"), row(1, "2025-01-09", "newest"), row(1, "2025-01-01", "old")]
    assert dedupe_latest(rows) == [row(1, "2025-01-09", "newest")]


def test_one_row_per_id_sorted_by_id():
    rows = [row(3, "2025-01-01"), row(1, "2025-01-01"), row(2, "2025-01-01")]
    assert [r["id"] for r in dedupe_latest(rows)] == [1, 2, 3]


def test_tie_goes_to_later_row():
    rows = [row(1, "2025-01-01", "first"), row(1, "2025-01-01", "second")]
    assert dedupe_latest(rows)[0]["v"] == "second"


def test_none_is_older_than_a_timestamp():
    rows = [row(1, "2025-01-01", "real"), row(1, None, "missing")]
    assert dedupe_latest(rows)[0]["v"] == "real"
    rows = [row(1, None, "missing"), row(1, "2025-01-01", "real")]
    assert dedupe_latest(rows)[0]["v"] == "real"


def test_single_row_with_none_is_kept():
    assert dedupe_latest([row(1, None, "only")]) == [row(1, None, "only")]


def test_input_is_not_modified():
    rows = [row(2, "2025-01-02"), row(1, "2025-01-01"), row(2, "2025-01-03")]
    before = copy.deepcopy(rows)
    dedupe_latest(rows)
    assert rows == before


def test_empty_input():
    assert dedupe_latest([]) == []
