from solution import line_spread


def write(tmp_path, text):
    p = tmp_path / "t.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_example(tmp_path):
    p = write(tmp_path, "the cat and the hat\na cat\n")
    assert line_spread(p) == {"the": 1, "cat": 2, "and": 1, "hat": 1, "a": 1}


def test_repeat_on_one_line(tmp_path):
    assert line_spread(write(tmp_path, "go go go\n")) == {"go": 1}


def test_case_and_punctuation(tmp_path):
    p = write(tmp_path, "Hello, world!\nHELLO again.\n")
    assert line_spread(p) == {"hello": 2, "world": 1, "again": 1}


def test_blank_lines(tmp_path):
    assert line_spread(write(tmp_path, "\n\nx\n\n")) == {"x": 1}


def test_empty_file(tmp_path):
    assert line_spread(write(tmp_path, "")) == {}
