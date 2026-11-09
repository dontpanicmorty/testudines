from solution import read_clean


def test_basic(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("  tea\ncoffee\n", encoding="utf-8")
    assert read_clean(p) == ["  tea", "coffee"]


def test_empty_file(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("", encoding="utf-8")
    assert read_clean(p) == []


def test_blank_line_kept(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("a\n\nb", encoding="utf-8")
    assert read_clean(p) == ["a", "", "b"]


def test_accents(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("caf\u00e9\n", encoding="utf-8")
    assert read_clean(p) == ["caf\u00e9"]
