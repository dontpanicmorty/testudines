from solution import build_url


def test_basic():
    assert build_url("http://x.test/find", {"q": "red bike", "n": 3}) == "http://x.test/find?q=red+bike&n=3"


def test_empty_params():
    assert build_url("http://x.test/find", {}) == "http://x.test/find"


def test_ampersand_escaped():
    assert build_url("http://x.test/s", {"q": "a&b=c"}) == "http://x.test/s?q=a%26b%3Dc"


def test_order_kept():
    assert build_url("http://x.test", {"b": 1, "a": 2}) == "http://x.test?b=1&a=2"
