import pytest

from solution import LoadError, RowError, SchemaError, load_rows


def test_happy_path():
    lines = ["id, amount\n", "1,5\n", "2, 7\n"]
    assert load_rows(lines) == [{"id": "1", "amount": "5"}, {"id": "2", "amount": "7"}]


def test_extra_columns_allowed_and_blank_lines_skipped():
    lines = ["id,amount,note", "", "1,5,hi", "   ", "2,6,yo"]
    rows = load_rows(lines)
    assert [r["note"] for r in rows] == ["hi", "yo"]


def test_hierarchy():
    assert issubclass(SchemaError, LoadError)
    assert issubclass(RowError, LoadError)
    assert issubclass(LoadError, Exception)


def test_missing_columns_error():
    with pytest.raises(SchemaError) as info:
        load_rows(["name,amount", "x,1"])
    assert info.value.missing == ["id"]
    assert str(info.value) == "missing columns: id"


def test_multiple_missing_are_sorted():
    with pytest.raises(SchemaError) as info:
        load_rows(["name"])
    assert info.value.missing == ["amount", "id"]
    assert str(info.value) == "missing columns: amount, id"


def test_empty_input_is_a_schema_error():
    with pytest.raises(SchemaError) as info:
        load_rows([])
    assert info.value.missing == ["amount", "id"]


def test_row_error_has_line_number_and_message():
    with pytest.raises(RowError) as info:
        load_rows(["id,amount,note", "1,5,x", "2,6"])
    assert info.value.line_number == 3
    assert str(info.value) == "line 3: expected 3 fields, got 2"


def test_line_numbers_count_blank_lines():
    with pytest.raises(RowError) as info:
        load_rows(["id,amount", "", "1,5,extra"])
    assert info.value.line_number == 3


def test_caller_can_catch_the_base_class():
    with pytest.raises(LoadError):
        load_rows(["id,amount", "1"])


def test_custom_required_columns():
    assert load_rows(["a,b", "1,2"], required=("a",)) == [{"a": "1", "b": "2"}]
