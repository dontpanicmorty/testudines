from solution import apply_corrections


def test_result_is_corrected():
    rows = [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}]
    out = apply_corrections(rows, [(0, "plan", "pro")])
    assert out == [{"id": 1, "plan": "pro"}, {"id": 2, "plan": "pro"}]


def test_original_untouched():
    rows = [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}]
    apply_corrections(rows, [(0, "plan", "pro")])
    assert rows == [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}], "input rows were mutated"


def test_returns_new_list():
    rows = [{"id": 1}]
    assert apply_corrections(rows, []) is not rows


def test_multiple_fixes_and_new_field():
    rows = [{"id": 1}, {"id": 2}]
    out = apply_corrections(rows, [(1, "x", 1), (1, "x", 2), (0, "y", 3)])
    assert out == [{"id": 1, "y": 3}, {"id": 2, "x": 2}]
    assert rows == [{"id": 1}, {"id": 2}]
