import dataclasses

from solution import ColumnSpec, describe


def test_is_a_dataclass_with_defaults():
    assert dataclasses.is_dataclass(ColumnSpec)
    c = ColumnSpec("a", "int")
    assert c.nullable is True
    assert c.tags == []


def test_tags_are_not_shared():
    a, b = ColumnSpec("a", "int"), ColumnSpec("b", "int")
    a.tags.append("key")
    assert b.tags == []


def test_equality_and_repr():
    assert ColumnSpec("a", "int") == ColumnSpec("a", "int")
    assert ColumnSpec("a", "int") != ColumnSpec("a", "str")
    assert "ColumnSpec(name='a'" in repr(ColumnSpec("a", "int"))


def test_describe():
    assert describe(ColumnSpec("order_id", "int", nullable=False, tags=["key"])) == "order_id: int (not null)"
    assert describe(ColumnSpec("note", "str")) == "note: str"
