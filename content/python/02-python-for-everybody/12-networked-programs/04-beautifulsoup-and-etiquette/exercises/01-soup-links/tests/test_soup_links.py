from solution import hrefs_in


def test_basic():
    html = '<a href="/a">A</a><a href=\'/b\' class="x">B</a>'
    assert hrefs_in(html) == ["/a", "/b"]


def test_anchor_without_href():
    assert hrefs_in('<a name="top">t</a><a href="/z">z</a>') == ["/z"]


def test_uppercase_and_attribute_order():
    assert hrefs_in('<A CLASS="c" HREF="/up">u</A>') == ["/up"]


def test_none():
    assert hrefs_in("<p>nothing</p>") == []


def test_line_break_inside_tag():
    assert hrefs_in('<a\n  href="/lb">x</a>') == ["/lb"]
