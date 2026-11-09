"""Freshness checks with an injectable clock."""
from datetime import datetime, timedelta, timezone


def _current(now):
    return now() if now is not None else datetime.now(timezone.utc)


def is_late(expected_by, *, now=None, grace_minutes=0):
    return _current(now) > expected_by + timedelta(minutes=grace_minutes)


def minutes_late(expected_by, *, now=None):
    delta = _current(now) - expected_by
    if delta <= timedelta(0):
        return 0
    return int(delta.total_seconds() // 60)
