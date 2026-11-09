from datetime import date, datetime, timedelta, timezone

from solution import event_day, to_utc


def test_offset():
    out = to_utc("2025-06-05T23:30:00+02:00")
    assert out == datetime(2025, 6, 5, 21, 30, tzinfo=timezone.utc)
    assert out.utcoffset() == timedelta(0)


def test_naive_assumed_utc():
    out = to_utc("2025-06-05T00:48:57")
    assert out.tzinfo is not None
    assert out == datetime(2025, 6, 5, 0, 48, 57, tzinfo=timezone.utc)


def test_z_suffix():
    assert to_utc("2025-06-05T10:00:00Z") == datetime(2025, 6, 5, 10, 0, tzinfo=timezone.utc)


def test_event_day_uses_utc():
    assert event_day("2025-06-06T01:00:00+05:00") == date(2025, 6, 5)
    assert event_day("2025-06-05T23:30:00-03:00") == date(2025, 6, 6)


def test_results_are_comparable():
    a = to_utc("2025-06-05T00:00:00")
    b = to_utc("2025-06-05T00:00:00+01:00")
    assert b < a
