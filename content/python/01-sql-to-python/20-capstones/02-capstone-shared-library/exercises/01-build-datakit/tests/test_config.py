from dataclasses import dataclass, field

import pytest

from datakit import ConfigError, DatakitError, load_config


@dataclass(frozen=True)
class Settings:
    db_path: str
    max_rows: int = 100
    ratio: float = 0.5
    debug: bool = False
    note: str | None = None


def test_reads_and_converts_types():
    env = {"DB_PATH": "a.db", "MAX_ROWS": "250", "RATIO": "1.25", "DEBUG": "true", "NOTE": "hi"}
    cfg = load_config(Settings, env)
    assert cfg == Settings("a.db", 250, 1.25, True, "hi")
    assert type(cfg.max_rows) is int and type(cfg.ratio) is float


def test_defaults_apply_when_missing():
    cfg = load_config(Settings, {"DB_PATH": "a.db"})
    assert (cfg.max_rows, cfg.ratio, cfg.debug, cfg.note) == (100, 0.5, False, None)


def test_prefix():
    cfg = load_config(Settings, {"APP_DB_PATH": "p.db", "DB_PATH": "wrong.db"}, prefix="APP_")
    assert cfg.db_path == "p.db"


@pytest.mark.parametrize("raw,expected", [
    ("1", True), ("TRUE", True), ("Yes", True), ("on", True),
    ("0", False), ("false", False), ("NO", False), ("off", False), (" true ", True),
])
def test_bool_spellings(raw, expected):
    assert load_config(Settings, {"DB_PATH": "x", "DEBUG": raw}).debug is expected


def test_missing_required_names_the_key():
    with pytest.raises(ConfigError) as exc:
        load_config(Settings, {})
    assert exc.value.errors == ["DB_PATH: missing"]
    assert "DB_PATH" in str(exc.value)


def test_all_problems_reported_together_in_field_order():
    with pytest.raises(ConfigError) as exc:
        load_config(Settings, {"MAX_ROWS": "many", "DEBUG": "maybe"})
    errs = exc.value.errors
    assert len(errs) == 3
    assert errs[0].startswith("DB_PATH")
    assert errs[1].startswith("MAX_ROWS") and "'many'" in errs[1] and "int" in errs[1]
    assert errs[2].startswith("DEBUG")


def test_config_error_is_a_datakit_error():
    assert issubclass(ConfigError, DatakitError)


def test_int_with_whitespace_and_float_for_int_rejected():
    assert load_config(Settings, {"DB_PATH": "x", "MAX_ROWS": " 7 "}).max_rows == 7
    with pytest.raises(ConfigError):
        load_config(Settings, {"DB_PATH": "x", "MAX_ROWS": "7.5"})


def test_empty_string_is_a_value_for_str():
    assert load_config(Settings, {"DB_PATH": ""}).db_path == ""


def test_default_source_is_os_environ(monkeypatch):
    monkeypatch.setenv("DB_PATH", "env.db")
    monkeypatch.setenv("MAX_ROWS", "5")
    cfg = load_config(Settings)
    assert (cfg.db_path, cfg.max_rows) == ("env.db", 5)


def test_default_factory_fields():
    @dataclass
    class WithFactory:
        tags: list = field(default_factory=list)
        name: str = "n"

    assert load_config(WithFactory, {}).tags == []


def test_not_a_dataclass_is_a_type_error():
    class Plain:
        pass

    with pytest.raises(TypeError):
        load_config(Plain, {})


def test_source_not_mutated():
    env = {"DB_PATH": "x"}
    load_config(Settings, env)
    assert env == {"DB_PATH": "x"}
