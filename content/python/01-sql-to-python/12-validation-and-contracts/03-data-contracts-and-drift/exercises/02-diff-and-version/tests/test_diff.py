import pytest
from solution import diff_schemas, is_backward_compatible, next_version

OLD = {"id": "int", "email": "str", "mrr": "int"}


def test_diff():
    new = {"id": "int", "mail": "str", "mrr": "float", "plan": "str"}
    assert diff_schemas(OLD, new) == {
        "added": ["mail", "plan"], "removed": ["email"], "retyped": {"mrr": ("int", "float")}}


def test_diff_identical():
    assert diff_schemas(OLD, dict(OLD)) == {"added": [], "removed": [], "retyped": {}}


@pytest.mark.parametrize("new, ok", [
    ({**OLD, "plan": "str"}, True),
    ({**OLD, "mrr": "float"}, True),
    ({"id": "int", "mrr": "int"}, False),
    ({**OLD, "mrr": "str"}, False),
    ({**OLD, "id": "float", "mrr": "int"}, True),
    ({"id": "str", "email": "str", "mrr": "int"}, False),
])
def test_compat(new, ok):
    assert is_backward_compatible(OLD, new) is ok


def test_float_to_int_is_breaking():
    assert is_backward_compatible({"a": "float"}, {"a": "int"}) is False


@pytest.mark.parametrize("new, expected", [
    (dict(OLD), "1.4.2"),
    ({**OLD, "plan": "str"}, "1.5.0"),
    ({**OLD, "mrr": "float"}, "1.5.0"),
    ({"id": "int", "mrr": "int"}, "2.0.0"),
])
def test_next_version(new, expected):
    assert next_version("1.4.2", OLD, new) == expected
