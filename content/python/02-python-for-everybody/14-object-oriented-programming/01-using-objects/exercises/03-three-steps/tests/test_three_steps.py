from solution import report


def test_example():
    assert report("asha,30\nben,45\nasha,25") == "asha: 55\nben: 45"


def test_tie_broken_by_name():
    assert report("zoe,10\namy,10") == "amy: 10\nzoe: 10"


def test_blank_lines_ignored():
    assert report("\nasha,5\n\n") == "asha: 5"


def test_empty():
    assert report("") == ""
