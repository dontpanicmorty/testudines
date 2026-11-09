from solution import tidy


def test_basic():
    assert tidy(["  maya ", "TOMAS", "   ", "ana maria"]) == ["Maya", "Tomas", "Ana Maria"]


def test_all_blank():
    assert tidy(["", "  ", "\t"]) == []


def test_empty_list():
    assert tidy([]) == []


def test_already_tidy():
    assert tidy(["Priya"]) == ["Priya"]


def test_order_kept():
    assert tidy(["b", "a"]) == ["B", "A"]
