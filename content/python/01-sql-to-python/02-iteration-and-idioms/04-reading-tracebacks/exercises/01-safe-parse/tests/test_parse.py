from solution import parse_amounts


def test_mixed():
    assert parse_amounts(["1.5", " 2 ", "N/A", None, "3"]) == ([1.5, 2.0, 3.0], [(2, "N/A"), (3, None)])


def test_all_good_and_all_bad():
    assert parse_amounts(["1"]) == ([1.0], [])
    assert parse_amounts(["", "x"]) == ([], [(0, ""), (1, "x")])


def test_numbers_pass_through():
    assert parse_amounts([5, 2.5]) == ([5.0, 2.5], [])


def test_empty():
    assert parse_amounts([]) == ([], [])
