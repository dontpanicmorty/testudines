import pytest

from solution import connection_params, describe

CFG = {"account": "acme", "user": "svc_etl", "password_env": "WH_PASSWORD", "warehouse": "LOAD_WH"}


def test_params():
    p = connection_params(CFG, {"WH_PASSWORD": "s3cret"})
    assert p == {"account": "acme", "user": "svc_etl", "warehouse": "LOAD_WH", "password": "s3cret"}


def test_missing_secret_names_variable():
    with pytest.raises(RuntimeError) as exc:
        connection_params(CFG, {})
    assert "WH_PASSWORD" in str(exc.value)


def test_empty_secret_is_missing():
    with pytest.raises(RuntimeError):
        connection_params(CFG, {"WH_PASSWORD": ""})


def test_describe_is_safe():
    text = describe(CFG)
    assert "acme" in text and "svc_etl" in text and "LOAD_WH" in text
    assert "WH_PASSWORD" in text
    assert "\n" not in text


def test_describe_never_leaks_even_if_cfg_has_password():
    leaky = dict(CFG, password="s3cret")
    assert "s3cret" not in describe(leaky)
