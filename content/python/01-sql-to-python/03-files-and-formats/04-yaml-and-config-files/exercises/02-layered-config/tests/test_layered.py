from solution import build_config

DEFAULTS = {"retries": 3, "debug": False, "region": "eu", "db": {"host": "h", "port": 1}}


def test_example():
    out = build_config(DEFAULTS, {"db": {"host": "prod"}}, {"APP_RETRIES": "5"})
    assert out == {"retries": 5, "debug": False, "region": "eu", "db": {"host": "prod", "port": 1}}


def test_env_beats_file():
    out = build_config(DEFAULTS, {"region": "us"}, {"APP_REGION": "ap"})
    assert out["region"] == "ap"


def test_bool_conversion():
    assert build_config(DEFAULTS, {}, {"APP_DEBUG": "True"})["debug"] is True
    assert build_config(DEFAULTS, {}, {"APP_DEBUG": "no"})["debug"] is False


def test_prefix_and_unrelated_env():
    out = build_config(DEFAULTS, {}, {"OTHER_RETRIES": "9", "X_RETRIES": "7"}, prefix="X_")
    assert out["retries"] == 7


def test_inputs_not_mutated():
    d = {"db": {"host": "h"}}
    f = {"db": {"host": "p"}}
    build_config(d, f, {})
    assert d == {"db": {"host": "h"}}
    assert f == {"db": {"host": "p"}}
