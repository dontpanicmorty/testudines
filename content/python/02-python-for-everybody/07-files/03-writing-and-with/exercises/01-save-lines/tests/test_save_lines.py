from solution import save_lines


def test_basic(tmp_path):
    p = tmp_path / "o.txt"
    save_lines(p, ["eggs", "milk"])
    assert p.read_text(encoding="utf-8") == "eggs\nmilk\n"


def test_empty_list(tmp_path):
    p = tmp_path / "o.txt"
    save_lines(p, [])
    assert p.read_text(encoding="utf-8") == ""


def test_overwrites(tmp_path):
    p = tmp_path / "o.txt"
    p.write_text("old stuff that is long\n", encoding="utf-8")
    save_lines(p, ["new"])
    assert p.read_text(encoding="utf-8") == "new\n"


def test_accents(tmp_path):
    p = tmp_path / "o.txt"
    save_lines(p, ["cr\u00e8me"])
    assert p.read_text(encoding="utf-8") == "cr\u00e8me\n"
