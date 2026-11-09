"""Freshness checks with an injectable clock."""
from datetime import datetime, timedelta, timezone


def is_late(expected_by, *, now=None, grace_minutes=0):
    raise NotImplementedError


def minutes_late(expected_by, *, now=None):
    raise NotImplementedError
