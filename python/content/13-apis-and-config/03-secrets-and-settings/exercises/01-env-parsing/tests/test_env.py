import pytest

from solution import ConfigError, get_int, parse_bool


@pytest.mark.parametrize("text", ["1", "true", "TRUE", " Yes ", "on"])
def test_truthy(text):
    assert parse_bool(text) is True


@pytest.mark.parametrize("text", ["0", "false", "False", "no", " off", ""])
def test_falsy(text):
    assert parse_bool(text) is False


def test_bad_bool():
    with pytest.raises(ValueError):
        parse_bool("maybe")


def test_get_int_present_absent():
    assert get_int({"A": "500"}, "A", 1) == 500
    assert get_int({}, "A", 100) == 100


def test_get_int_bad_value_names_variable():
    with pytest.raises(ConfigError) as info:
        get_int({"APP_BATCH": "lots"}, "APP_BATCH", 1)
    assert "APP_BATCH" in str(info.value)
