from solution import evaluate_run


def m(**kw):
    base = {"rows_written": 500, "previous_rows": 500, "rows_rejected": 0,
            "latest_record": "2026-01-02T08:00:00", "now": "2026-01-02T09:00:00"}
    base.update(kw)
    return base


def test_healthy():
    assert evaluate_run(m()) == []


def test_stale_boundary_is_strict():
    assert evaluate_run(m(latest_record="2026-01-01T09:00:00")) == []
    assert evaluate_run(m(latest_record="2026-01-01T08:59:59")) == ["stale"]


def test_no_latest_record_is_stale():
    assert evaluate_run(m(latest_record=None)) == ["stale"]


def test_volume_drop_and_spike():
    assert evaluate_run(m(rows_written=100)) == ["volume_drop"]
    assert evaluate_run(m(rows_written=1200)) == ["volume_spike"]
    assert evaluate_run(m(rows_written=250)) == []
    assert evaluate_run(m(rows_written=1000)) == []


def test_no_baseline_skips_volume():
    assert evaluate_run(m(previous_rows=None, rows_written=1)) == []
    assert evaluate_run(m(previous_rows=0, rows_written=1)) == []


def test_reject_rate():
    assert evaluate_run(m(rows_written=95, rows_rejected=5, previous_rows=100)) == []
    assert evaluate_run(m(rows_written=90, rows_rejected=10, previous_rows=100)) == ["rejects"]


def test_combined_order():
    out = evaluate_run(m(rows_written=10, rows_rejected=10, latest_record=None))
    assert out == ["stale", "volume_drop", "rejects"]


def test_custom_thresholds():
    assert evaluate_run(m(latest_record="2026-01-02T01:00:00"), max_age_hours=6) == ["stale"]


def test_zero_rows_and_rejects():
    out = evaluate_run(m(rows_written=0, rows_rejected=0, previous_rows=None))
    assert out == []
