import inspect

import pytest

from reportkit import summarize

ROWS = [{"region": r} for r in ["eu", "us", "eu", "apac", "us", "eu"]]


def test_existing_behaviour_unchanged():
    assert summarize(ROWS, "region") == [("eu", 3), ("us", 2), ("apac", 1)]
    assert summarize(ROWS, key="region") == [("eu", 3), ("us", 2), ("apac", 1)]


def test_top_n():
    assert summarize(ROWS, "region", top_n=2) == [("eu", 3), ("us", 2)]
    assert summarize(ROWS, "region", top_n=1) == [("eu", 3)]
    assert summarize(ROWS, "region", top_n=0) == []
    assert summarize(ROWS, "region", top_n=10) == [("eu", 3), ("us", 2), ("apac", 1)]


def test_top_n_is_keyword_only_with_default():
    p = inspect.signature(summarize).parameters["top_n"]
    assert p.kind is inspect.Parameter.KEYWORD_ONLY
    assert p.default is None


def test_positional_top_n_rejected():
    with pytest.raises(TypeError):
        summarize(ROWS, "region", 2)
