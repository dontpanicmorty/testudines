from solution import link_targets


def test_basic():
    assert link_targets('<a href="/a">A</a> <a href="/b">B</a>') == ["/a", "/b"]


def test_none():
    assert link_targets("<p>no links</p>") == []


def test_same_line_not_merged():
    html = '<a href="x">1</a><a href="y">2</a>'
    assert link_targets(html) == ["x", "y"]


def test_other_attributes_before():
    assert link_targets('<a class="big" href="/z">Z</a>') == ["/z"]


def test_empty_href():
    assert link_targets('<a href="">e</a>') == [""]
