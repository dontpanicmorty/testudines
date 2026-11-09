from solution import hashtags


def test_basic():
    assert hashtags("Loving #python and #learn_2_code! # alone") == ["#python", "#learn_2_code"]


def test_none():
    assert hashtags("nothing to see") == []


def test_lone_hash():
    assert hashtags("# and #") == []


def test_adjacent():
    assert hashtags("#a#b") == ["#a", "#b"]


def test_punctuation_ends_tag():
    assert hashtags("#one, #two. #three?") == ["#one", "#two", "#three"]
