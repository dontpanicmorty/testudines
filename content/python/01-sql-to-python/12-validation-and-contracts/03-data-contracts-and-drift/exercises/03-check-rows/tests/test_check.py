from solution import check_rows

CONTRACT = {"id": "int", "email": "str", "mrr": "float"}


def test_clean():
    assert check_rows(CONTRACT, [{"id": 1, "email": "a@x", "mrr": 1.5}, {"id": 2, "email": None, "mrr": 3}]) == []


def test_each_problem_kind():
    rows = [{"id": "1", "email": "a@x", "mrr": 1.0, "extra": 5}, {"id": 2, "mrr": 1.0}]
    assert check_rows(CONTRACT, rows) == [
        (0, "extra", "unexpected"), (0, "id", "wrong_type"), (1, "email", "missing")]


def test_bool_is_not_int():
    assert check_rows({"id": "int"}, [{"id": True}]) == [(0, "id", "wrong_type")]


def test_float_column_rejects_str_but_accepts_int():
    assert check_rows({"x": "float"}, [{"x": 2}, {"x": "2.0"}]) == [(1, "x", "wrong_type")]


def test_empty():
    assert check_rows(CONTRACT, []) == []
