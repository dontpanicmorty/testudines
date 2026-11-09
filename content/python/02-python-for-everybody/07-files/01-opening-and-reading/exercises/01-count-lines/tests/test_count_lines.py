from solution import line_count


def test_three_lines(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("flour 2\nsugar 1\nrice 5\n", encoding="utf-8")
    assert line_count(p) == 3


def test_no_trailing_newline(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("one\ntwo", encoding="utf-8")
    assert line_count(str(p)) == 2


def test_empty(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("", encoding="utf-8")
    assert line_count(p) == 0


def test_blank_lines_count(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("\n\n", encoding="utf-8")
    assert line_count(p) == 2
