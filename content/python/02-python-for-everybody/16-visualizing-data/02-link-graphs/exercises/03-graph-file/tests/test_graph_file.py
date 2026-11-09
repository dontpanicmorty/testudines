import json

import pytest

from solution import graph_json


def test_symmetric_pair():
    data = json.loads(graph_json({"a": ["b"], "b": ["a"]}))
    assert data["nodes"] == [{"id": "a", "rank": 0.5}, {"id": "b", "rank": 0.5}]
    assert data["links"] == [{"source": "a", "target": "b"}, {"source": "b", "target": "a"}]


def test_popular_page_wins():
    links = {"home": ["news"], "news": ["home"], "about": ["home", "news"]}
    data = json.loads(graph_json(links))
    ranks = {n["id"]: n["rank"] for n in data["nodes"]}
    assert ranks["about"] < ranks["news"] < ranks["home"] or ranks["about"] < ranks["home"]
    assert sum(ranks.values()) == pytest.approx(1.0, abs=0.001)
    assert [n["id"] for n in data["nodes"]] == ["about", "home", "news"]


def test_empty_graph():
    assert json.loads(graph_json({})) == {"nodes": [], "links": []}


def test_single_page_no_links():
    data = json.loads(graph_json({"solo": []}))
    assert data["nodes"] == [{"id": "solo", "rank": 1.0}]
    assert data["links"] == []


def test_dangling_page_gets_share():
    data = json.loads(graph_json({"a": ["b"], "b": []}, rounds=1, damping=0.5))
    ranks = {n["id"]: n["rank"] for n in data["nodes"]}
    # base .25 each; a gives .5*.5 to b; b gives .5*.5/2 to each
    assert ranks["a"] == pytest.approx(0.375, abs=1e-4)
    assert ranks["b"] == pytest.approx(0.625, abs=1e-4)


def test_returns_text():
    assert isinstance(graph_json({"a": []}), str)
