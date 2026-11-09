from datetime import datetime, timezone

import pytest

from solution import is_late, minutes_late

DUE = datetime(2025, 1, 1, 6, 0, tzinfo=timezone.utc)


def at(h, m, s=0):
    return lambda: datetime(2025, 1, 1, h, m, s, tzinfo=timezone.utc)


def test_not_late_before_deadline():
    assert is_late(DUE, now=at(5, 59)) is False


def test_exactly_on_deadline_is_not_late():
    assert is_late(DUE, now=at(6, 0)) is False


def test_late_after_deadline():
    assert is_late(DUE, now=at(6, 0, 1)) is True


def test_grace_period():
    assert is_late(DUE, now=at(6, 45), grace_minutes=60) is False
    assert is_late(DUE, now=at(7, 1), grace_minutes=60) is True


@pytest.mark.parametrize(
    "clock, expected",
    [(at(5, 0), 0), (at(6, 0), 0), (at(6, 0, 59), 0), (at(6, 1), 1), (at(6, 45, 30), 45), (at(8, 0), 120)],
)
def test_minutes_late(clock, expected):
    assert minutes_late(DUE, now=clock) == expected


def test_default_clock_is_real_time():
    assert is_late(datetime(2000, 1, 1, tzinfo=timezone.utc)) is True
    assert is_late(datetime(2999, 1, 1, tzinfo=timezone.utc)) is False
    assert minutes_late(datetime(2999, 1, 1, tzinfo=timezone.utc)) == 0
