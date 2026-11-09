from solution import merge_tables


def test_basic():
    assert merge_tables([[1, 2]], [[3], [4, 5]]) == [[1, 2], [3], [4, 5]]


def test_rows_are_copies():
    a = [[1, 2]]
    b = [[3]]
    result = merge_tables(a, b)
    result[0][0] = 99
    result[1].append(7)
    assert a == [[1, 2]]
    assert b == [[3]]


def test_arguments_unchanged():
    a = [[1]]
    b = [[2]]
    merge_tables(a, b)
    assert a == [[1]] and b == [[2]]


def test_empty_inputs():
    assert merge_tables([], []) == []
    assert merge_tables([], [[1]]) == [[1]]
