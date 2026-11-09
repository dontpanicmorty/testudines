import pytest

from solution import RunStats


def test_starts_at_zero():
    s = RunStats()
    assert (s.rows_read, s.rows_rejected) == (0, 0)


def test_record():
    s = RunStats()
    for ok in [True, False, True, False, False]:
        s.record(ok)
    assert (s.rows_read, s.rows_rejected) == (5, 3)


def test_reject_rate():
    s = RunStats()
    for ok in [True, False, True, True]:
        s.record(ok)
    assert s.reject_rate == pytest.approx(0.25)


def test_reject_rate_with_no_rows():
    assert RunStats().reject_rate == 0.0


def test_repr():
    s = RunStats()
    for ok in [True, False, True]:
        s.record(ok)
    assert repr(s) == "RunStats(read=3, rejected=1)"


def test_instances_are_independent():
    a, b = RunStats(), RunStats()
    a.record(False)
    assert b.rows_read == 0
