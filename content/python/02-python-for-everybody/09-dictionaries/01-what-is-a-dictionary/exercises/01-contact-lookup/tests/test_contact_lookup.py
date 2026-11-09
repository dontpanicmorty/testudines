from solution import find_number


def test_found():
    assert find_number({"Maya": "555-0101"}, "Maya") == "555-0101"


def test_missing():
    assert find_number({"Maya": "555-0101"}, "Priya") == "unknown"


def test_case_matters():
    assert find_number({"Maya": "1"}, "maya") == "unknown"


def test_empty_book():
    assert find_number({}, "Anyone") == "unknown"


def test_does_not_modify_book():
    book = {"A": "1"}
    find_number(book, "B")
    assert book == {"A": "1"}
