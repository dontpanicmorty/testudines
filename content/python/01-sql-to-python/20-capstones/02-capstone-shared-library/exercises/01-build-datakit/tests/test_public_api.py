"""Backward-compatibility guard: this is the contract version 1.x promises to consumers.

If you rename, remove or reorder anything checked here you would break your users.
"""
import inspect
import re

import datakit

EXPECTED_ALL = {
    "ConfigError", "ConnectionProtocol", "DatabaseError", "DatakitError",
    "RowValidator", "SqliteConnection", "load_config", "retry",
}


def test_all_is_exactly_the_documented_surface():
    assert set(datakit.__all__) == EXPECTED_ALL


def test_every_exported_name_exists_and_is_public():
    for name in datakit.__all__:
        assert not name.startswith("_"), name
        assert hasattr(datakit, name), name


def test_star_import_gives_the_public_names():
    ns: dict = {}
    exec("from datakit import *", ns)
    assert EXPECTED_ALL <= set(ns)


def test_version_is_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", datakit.__version__)
    assert datakit.__version__.startswith("1.")


def test_load_config_signature():
    sig = inspect.signature(datakit.load_config)
    assert list(sig.parameters) == ["cls", "source", "prefix"]
    assert sig.parameters["source"].default is None
    assert sig.parameters["prefix"].default == ""


def test_retry_signature_and_defaults():
    sig = inspect.signature(datakit.retry)
    assert list(sig.parameters) == ["attempts", "delay", "backoff", "exceptions", "sleep"]
    d = {k: p.default for k, p in sig.parameters.items()}
    assert d["attempts"] == 3 and d["delay"] == 0.0 and d["backoff"] == 2.0
    assert d["exceptions"] == (Exception,)


def test_row_validator_is_keyword_only_with_expected_names():
    sig = inspect.signature(datakit.RowValidator.__init__)
    params = [p for n, p in sig.parameters.items() if n != "self"]
    assert [p.name for p in params] == ["required", "types", "checks"]
    assert all(p.kind is inspect.Parameter.KEYWORD_ONLY for p in params)
    assert hasattr(datakit.RowValidator, "errors") and hasattr(datakit.RowValidator, "split")


def test_connection_protocol_members():
    members = {n for n in dir(datakit.ConnectionProtocol) if not n.startswith("_")}
    assert {"query", "execute", "close"} <= members
    for name in ("query", "execute", "close"):
        assert hasattr(datakit.SqliteConnection, name)
    assert hasattr(datakit.SqliteConnection, "transaction")
    assert hasattr(datakit.SqliteConnection, "executemany")


def test_exception_hierarchy():
    assert issubclass(datakit.DatakitError, Exception)
    assert issubclass(datakit.ConfigError, datakit.DatakitError)
    assert issubclass(datakit.DatabaseError, datakit.DatakitError)


def test_public_things_have_docstrings():
    for name in ("load_config", "retry", "RowValidator", "SqliteConnection", "ConnectionProtocol", "DatakitError"):
        obj = getattr(datakit, name)
        assert inspect.getdoc(obj), f"{name} needs a docstring"


def test_public_functions_are_annotated():
    for fn in (datakit.load_config, datakit.retry):
        sig = inspect.signature(fn)
        assert sig.return_annotation is not inspect.Signature.empty, f"{fn.__name__} needs a return annotation"
        for p in sig.parameters.values():
            assert p.annotation is not inspect.Parameter.empty, f"{fn.__name__}.{p.name} needs a type hint"


def test_library_code_does_not_print(capsys):
    import dataclasses

    @dataclasses.dataclass
    class C:
        a: int = 1

    datakit.load_config(C, {})
    datakit.RowValidator(required=["a"]).split([{"a": 1}])
    datakit.retry(attempts=1)(lambda: 1)()
    with datakit.SqliteConnection() as c:
        c.execute("select 1")
    assert capsys.readouterr().out == ""
