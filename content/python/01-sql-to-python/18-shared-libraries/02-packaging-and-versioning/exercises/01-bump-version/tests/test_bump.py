import pytest

from solution import bump, is_newer


def test_bumps():
    assert bump("1.4.2", "patch") == "1.4.3"
    assert bump("1.4.2", "minor") == "1.5.0"
    assert bump("1.4.2", "major") == "2.0.0"


def test_double_digits():
    assert bump("1.4.9", "patch") == "1.4.10"
    assert bump("0.9.9", "minor") == "0.10.0"


def test_is_newer_numeric():
    assert is_newer("1.10.0", "1.9.0") is True
    assert is_newer("1.9.0", "1.10.0") is False
    assert is_newer("1.2.3", "1.2.3") is False
    assert is_newer("2.0.0", "1.99.99") is True


@pytest.mark.parametrize("bad", ["1.2", "a.b.c", "1.2.3.4", ""])
def test_bad_version(bad):
    with pytest.raises(ValueError):
        bump(bad, "patch")


def test_bad_part():
    with pytest.raises(ValueError):
        bump("1.0.0", "huge")
