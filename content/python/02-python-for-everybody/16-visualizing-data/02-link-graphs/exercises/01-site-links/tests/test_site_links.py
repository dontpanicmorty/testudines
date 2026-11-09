from solution import internal_links


def test_example():
    html = '<a href="b.html">B</a><a href="https://x.test">X</a><a href="b.html">again</a>'
    assert internal_links(html, {"a.html", "b.html"}) == ["b.html"]


def test_sorted_unique():
    html = '<a href="c.html">c</a> <a href="a.html">a</a> <a href="c.html">c</a>'
    assert internal_links(html, {"a.html", "c.html"}) == ["a.html", "c.html"]


def test_no_links():
    assert internal_links("<p>nothing here</p>", {"a.html"}) == []


def test_other_attributes_ignored():
    html = '<img src="a.html"><a class="x" href="a.html">a</a>'
    assert internal_links(html, {"a.html"}) == ["a.html"]
