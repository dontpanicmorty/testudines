import sys

import pytest

from solution import load_module_from


def make(folder, name, body):
    folder.mkdir(exist_ok=True)
    (folder / f"{name}.py").write_text(body)
    return folder


def test_loads_and_returns_module(tmp_path):
    d = make(tmp_path / "a", "plugin", "def run():\n    return 'a'\n")
    mod = load_module_from(d, "plugin")
    assert mod.run() == "a"


def test_accepts_str_path(tmp_path):
    d = make(tmp_path / "a", "plugin", "VALUE = 1\n")
    assert load_module_from(str(d), "plugin").VALUE == 1


def test_sys_path_restored(tmp_path):
    d = make(tmp_path / "a", "plugin", "VALUE = 1\n")
    before = list(sys.path)
    load_module_from(d, "plugin")
    assert sys.path == before, "sys.path was changed by the loader"


def test_sys_path_restored_on_error(tmp_path):
    d = make(tmp_path / "a", "plugin", "raise RuntimeError('boom')\n")
    before = list(sys.path)
    with pytest.raises(RuntimeError):
        load_module_from(d, "plugin")
    assert sys.path == before, "sys.path must be restored even when the plugin fails"


def test_two_directories_same_name(tmp_path):
    a = make(tmp_path / "a", "plugin", "WHO = 'team a'\n")
    b = make(tmp_path / "b", "plugin", "WHO = 'team b'\n")
    assert load_module_from(a, "plugin").WHO == "team a"
    assert load_module_from(b, "plugin").WHO == "team b"


def test_not_left_in_sys_modules(tmp_path):
    d = make(tmp_path / "a", "plugin_x", "VALUE = 1\n")
    load_module_from(d, "plugin_x")
    assert "plugin_x" not in sys.modules


def test_missing_module(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    with pytest.raises(ModuleNotFoundError):
        load_module_from(d, "does_not_exist_anywhere")
