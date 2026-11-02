from solution import count_records


def test_basic(tmp_path):
    p = tmp_path / "e.txt"
    p.write_text("a\n\n  \nb\nc\n", encoding="utf-8")
    assert count_records(p) == 3


def test_no_trailing_newline(tmp_path):
    p = tmp_path / "e.txt"
    p.write_text("a\nb", encoding="utf-8")
    assert count_records(p) == 2


def test_empty_file(tmp_path):
    p = tmp_path / "e.txt"
    p.write_text("", encoding="utf-8")
    assert count_records(p) == 0


def test_unicode(tmp_path):
    p = tmp_path / "e.txt"
    p.write_text("Zoë\nJosé\n", encoding="utf-8")
    assert count_records(p) == 2
