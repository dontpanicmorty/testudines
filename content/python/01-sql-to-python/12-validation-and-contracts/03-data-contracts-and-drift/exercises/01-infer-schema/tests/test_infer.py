from solution import infer_schema


def test_basic_and_order():
    rows = [{"id": 1, "x": None}, {"id": 2, "x": None, "y": 2.5}]
    out = infer_schema(rows)
    assert out == {"id": "int", "x": "null", "y": "float"}
    assert list(out) == ["id", "x", "y"]


def test_int_float_widening():
    assert infer_schema([{"v": 1}, {"v": 2.5}]) == {"v": "float"}


def test_other_mix_is_str():
    assert infer_schema([{"v": 1}, {"v": "a"}]) == {"v": "str"}
    assert infer_schema([{"v": True}, {"v": 1}]) == {"v": "str"}


def test_bool_stays_bool():
    assert infer_schema([{"v": True}, {"v": False}]) == {"v": "bool"}


def test_none_does_not_hide_type_and_empty():
    assert infer_schema([{"v": None}, {"v": "a"}]) == {"v": "str"}
    assert infer_schema([]) == {}
