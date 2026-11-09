from solution import headings


def test_basic():
    assert headings("<h1> Club </h1><p>x</p><h2>News</h2>") == ["Club", "News"]


def test_h3_ignored():
    assert headings("<h3>small</h3>") == []


def test_none():
    assert headings("") == []


def test_two_on_one_line_not_merged():
    assert headings("<h2>a</h2><h2>b</h2>") == ["a", "b"]


def test_order_preserved():
    assert headings("<h2>second</h2><h1>first</h1>") == ["second", "first"]
