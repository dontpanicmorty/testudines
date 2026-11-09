from solution import plan_incremental


def row(i, ts, v="x"):
    return {"id": i, "updated_at": ts, "v": v}


def test_first_run_dedupes_everything():
    rows = [row(2, "2026-01-01T10:00:00"), row(1, "2026-01-01T09:00:00", "old"),
            row(1, "2026-01-01T11:00:00", "new")]
    out = plan_incremental(rows, None, 3)
    assert [(r["id"], r["v"]) for r in out] == [(1, "new"), (2, "x")]


def test_lookback_includes_late_row():
    rows = [row(1, "2026-01-02T07:30:00"), row(2, "2026-01-02T05:00:00")]
    out = plan_incremental(rows, "2026-01-02T08:00:00", 1)
    assert [r["id"] for r in out] == [1]


def test_boundary_is_inclusive():
    rows = [row(1, "2026-01-02T07:00:00")]
    assert len(plan_incremental(rows, "2026-01-02T08:00:00", 1)) == 1


def test_lookback_crosses_midnight():
    rows = [row(1, "2026-01-01T23:30:00")]
    assert len(plan_incremental(rows, "2026-01-02T00:30:00", 2)) == 1


def test_zero_lookback_includes_equal_watermark():
    rows = [row(1, "2026-01-02T08:00:00"), row(2, "2026-01-02T07:59:59")]
    out = plan_incremental(rows, "2026-01-02T08:00:00", 0)
    assert [r["id"] for r in out] == [1]


def test_latest_version_wins_inside_window():
    rows = [row(1, "2026-01-02T07:10:00", "a"), row(1, "2026-01-02T07:50:00", "b")]
    out = plan_incremental(rows, "2026-01-02T08:00:00", 1)
    assert out[0]["v"] == "b" and len(out) == 1
