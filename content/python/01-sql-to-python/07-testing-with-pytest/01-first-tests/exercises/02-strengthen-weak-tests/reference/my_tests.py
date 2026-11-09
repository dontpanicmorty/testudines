import pytest

from status import normalize_status


@pytest.mark.parametrize("raw", ["active", "paused", "cancelled"])
def test_known_statuses_unchanged(raw):
    assert normalize_status(raw) == raw


def test_case_is_folded():
    assert normalize_status("Paused") == "paused"


def test_whitespace_is_stripped():
    assert normalize_status("  active ") == "active"


def test_none_is_unknown():
    assert normalize_status(None) == "unknown"


def test_blank_is_unknown():
    assert normalize_status("   ") == "unknown"


def test_unrecognised_is_unknown():
    assert normalize_status("archived") == "unknown"
