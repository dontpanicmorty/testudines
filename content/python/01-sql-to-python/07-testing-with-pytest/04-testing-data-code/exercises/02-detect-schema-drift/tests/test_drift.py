from solution import check_schema


def test_identical_schemas_have_no_problems():
    s = {"a": "int", "b": "str"}
    assert check_schema(s, dict(s)) == []


def test_missing_column():
    assert check_schema({"a": "int", "b": "str"}, {"a": "int"}) == ["missing column: b"]


def test_unexpected_column():
    assert check_schema({"a": "int"}, {"a": "int", "z": "str"}) == ["unexpected column: z"]


def test_type_change():
    assert check_schema({"a": "int"}, {"a": "str"}) == ["type changed: a int -> str"]


def test_multiple_problems_sorted_by_column():
    expected = {"order_id": "int", "total": "float"}
    actual = {"order_id": "str", "region": "str"}
    assert check_schema(expected, actual) == [
        "type changed: order_id int -> str",
        "unexpected column: region",
        "missing column: total",
    ]


def test_both_empty():
    assert check_schema({}, {}) == []


def test_inputs_not_modified():
    expected, actual = {"a": "int"}, {"b": "str"}
    check_schema(expected, actual)
    assert expected == {"a": "int"} and actual == {"b": "str"}
