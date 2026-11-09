from solution import total_stock


def test_basic(tmp_path):
    p = tmp_path / "s.txt"
    p.write_text("flour 2\nsugar 1\nrice 5\n", encoding="utf-8")
    assert total_stock(p) == 8


def test_blank_lines(tmp_path):
    p = tmp_path / "s.txt"
    p.write_text("\nflour 2\n\n   \nrice 10", encoding="utf-8")
    assert total_stock(p) == 12


def test_empty(tmp_path):
    p = tmp_path / "s.txt"
    p.write_text("", encoding="utf-8")
    assert total_stock(p) == 0


def test_extra_spaces(tmp_path):
    p = tmp_path / "s.txt"
    p.write_text("oats    4  \n", encoding="utf-8")
    assert total_stock(p) == 4
