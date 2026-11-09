from solution import running_totals


def test_basic():
    entries = [("a", "2025-01-01", 10), ("a", "2025-01-02", -4), ("b", "2025-01-01", 7)]
    assert running_totals(entries) == [
        ("a", "2025-01-01", 10, 10), ("a", "2025-01-02", -4, 6), ("b", "2025-01-01", 7, 7)]


def test_unsorted_input_and_accounts_independent():
    entries = [("b", "2025-02-01", 1), ("a", "2025-01-03", 5), ("a", "2025-01-01", 2),
               ("b", "2025-01-15", 100)]
    assert running_totals(entries) == [
        ("a", "2025-01-01", 2, 2), ("a", "2025-01-03", 5, 7),
        ("b", "2025-01-15", 100, 100), ("b", "2025-02-01", 1, 101)]


def test_empty():
    assert running_totals([]) == []


def test_python_ints_returned():
    out = running_totals([("a", "2025-01-01", 3)])
    assert type(out[0][2]) is int and type(out[0][3]) is int
