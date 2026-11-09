from solution import grep


def write(tmp_path, text):
    p = tmp_path / "log.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_anchor(tmp_path):
    p = write(tmp_path, "ERROR a\nINFO b\nxERROR c\n")
    assert grep(p, r"^ERROR") == ["ERROR a"]


def test_no_match(tmp_path):
    assert grep(write(tmp_path, "a\nb\n"), r"\d") == []


def test_empty_lines(tmp_path):
    assert grep(write(tmp_path, "a\n\nb\n"), r"^$") == [""]


def test_order_kept(tmp_path):
    p = write(tmp_path, "x1\ny\nx2\n")
    assert grep(p, r"x\d") == ["x1", "x2"]


def test_last_line_without_newline(tmp_path):
    assert grep(write(tmp_path, "one\ntwo"), "two") == ["two"]
