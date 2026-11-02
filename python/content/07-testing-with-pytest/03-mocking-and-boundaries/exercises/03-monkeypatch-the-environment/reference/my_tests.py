import pytest

from settings import ConfigError, connection_settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for name in ("DOJO_WAREHOUSE", "DOJO_SCHEMA", "DOJO_TIMEOUT"):
        monkeypatch.delenv(name, raising=False)


def test_defaults(monkeypatch):
    monkeypatch.setenv("DOJO_WAREHOUSE", "wh_test")
    assert connection_settings() == {"warehouse": "wh_test", "schema": "analytics", "timeout": 30}


def test_overrides(monkeypatch):
    monkeypatch.setenv("DOJO_WAREHOUSE", " wh ")
    monkeypatch.setenv("DOJO_SCHEMA", "staging")
    monkeypatch.setenv("DOJO_TIMEOUT", "5")
    assert connection_settings() == {"warehouse": "wh", "schema": "staging", "timeout": 5}


def test_missing_warehouse():
    with pytest.raises(ConfigError):
        connection_settings()


def test_blank_warehouse(monkeypatch):
    monkeypatch.setenv("DOJO_WAREHOUSE", "   ")
    with pytest.raises(ConfigError):
        connection_settings()


@pytest.mark.parametrize("bad", ["abc", "1.5", "", "0", "-3"])
def test_bad_timeout(monkeypatch, bad):
    monkeypatch.setenv("DOJO_WAREHOUSE", "wh")
    monkeypatch.setenv("DOJO_TIMEOUT", bad)
    with pytest.raises(ConfigError):
        connection_settings()


def test_timeout_one_is_valid(monkeypatch):
    monkeypatch.setenv("DOJO_WAREHOUSE", "wh")
    monkeypatch.setenv("DOJO_TIMEOUT", "1")
    assert connection_settings()["timeout"] == 1
