import pytest

from solution import topo_sort


def valid(graph, order):
    pos = {n: i for i, n in enumerate(order)}
    return sorted(order) == sorted(graph) and all(
        pos[d] < pos[n] for n, deps in graph.items() for d in deps
    )


def test_simple_chain():
    assert topo_sort({"b": ["a"], "a": [], "c": ["b"]}) == ["a", "b", "c"]


def test_deterministic_tie_break():
    g = {"z": [], "m": [], "a": ["z"]}
    assert topo_sort(g) == ["m", "z", "a"]


def test_diamond():
    g = {"top": [], "left": ["top"], "right": ["top"], "bottom": ["left", "right"]}
    out = topo_sort(g)
    assert valid(g, out)
    assert out == ["top", "left", "right", "bottom"]


def test_empty_graph():
    assert topo_sort({}) == []


def test_cycle():
    with pytest.raises(ValueError, match="cycle"):
        topo_sort({"a": ["b"], "b": ["c"], "c": ["a"]})


def test_cycle_with_valid_prefix():
    with pytest.raises(ValueError, match="cycle"):
        topo_sort({"ok": [], "a": ["b", "ok"], "b": ["a"]})


def test_missing_dependency():
    with pytest.raises(ValueError, match="ghost"):
        topo_sort({"a": ["ghost"]})


def test_input_not_modified():
    g = {"b": ["a"], "a": []}
    topo_sort(g)
    assert g == {"b": ["a"], "a": []}
