import copy

from solution import add_window_columns


def row(c, d, a):
    return {"customer": c, "day": d, "amount": a}


def test_example():
    out = add_window_columns([row("Ada", "2025-06-02", 70), row("Ada", "2025-06-01", 50)])
    assert out == [
        {**row("Ada", "2025-06-01", 50), "running_total": 50, "prev_amount": None},
        {**row("Ada", "2025-06-02", 70), "running_total": 120, "prev_amount": 50},
    ]


def test_partitions_reset():
    out = add_window_columns(
        [row("Bo", "2025-06-01", 20), row("Ada", "2025-06-01", 5), row("Bo", "2025-06-03", 1), row("Ada", "2025-06-04", 6)]
    )
    assert [(r["customer"], r["running_total"], r["prev_amount"]) for r in out] == [
        ("Ada", 5, None),
        ("Ada", 11, 5),
        ("Bo", 20, None),
        ("Bo", 21, 20),
    ]


def test_input_not_mutated():
    src = [row("Ada", "2025-06-02", 70), row("Ada", "2025-06-01", 50)]
    snapshot = copy.deepcopy(src)
    add_window_columns(src)
    assert src == snapshot


def test_stable_for_ties():
    out = add_window_columns([row("A", "d", 1), row("A", "d", 2), row("A", "d", 3)])
    assert [r["amount"] for r in out] == [1, 2, 3]
    assert [r["running_total"] for r in out] == [1, 3, 6]


def test_empty():
    assert add_window_columns([]) == []
