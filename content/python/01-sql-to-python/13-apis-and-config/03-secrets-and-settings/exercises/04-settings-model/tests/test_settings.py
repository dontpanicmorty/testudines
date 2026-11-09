import pytest

from solution import ConfigError, Settings, load_settings

GOOD = {"APP_API_URL": "https://x.test", "APP_API_TOKEN": "s3cret-value"}


def test_defaults_and_conversion():
    s = load_settings({**GOOD, "APP_BATCH_SIZE": "250", "APP_DEBUG": "true", "APP_TIMEOUT_S": "2.5", "PATH": "/bin"})
    assert (s.api_url, s.batch_size, s.debug, s.timeout_s) == ("https://x.test", 250, True, 2.5)
    d = load_settings(GOOD)
    assert (d.batch_size, d.debug, d.timeout_s) == (500, False, 10.0)


def test_secret_not_in_repr_or_str():
    s = load_settings(GOOD)
    assert "s3cret-value" not in repr(s)
    assert "s3cret-value" not in str(s)
    assert s.api_token.get_secret_value() == "s3cret-value"


def test_all_problems_listed():
    with pytest.raises(ConfigError) as info:
        load_settings({"APP_BATCH_SIZE": "lots"})
    msg = str(info.value)
    for name in ("APP_API_URL", "APP_API_TOKEN", "APP_BATCH_SIZE"):
        assert name in msg, f"{name} missing from: {msg}"


def test_token_value_not_leaked_in_error():
    with pytest.raises(ConfigError) as info:
        load_settings({"APP_API_URL": "u", "APP_API_TOKEN": "s3cret-value", "APP_BATCH_SIZE": "x"})
    assert "s3cret-value" not in str(info.value)


def test_settings_is_a_model():
    assert hasattr(Settings, "model_fields")
