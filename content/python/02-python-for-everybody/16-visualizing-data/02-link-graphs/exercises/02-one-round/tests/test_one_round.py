import pytest

from solution import rank_step


def close(a, b):
    assert set(a) == set(b)
    for k in a:
        assert a[k] == pytest.approx(b[k], abs=1e-9)


def test_two_pages_pointing_at_each_other():
    links = {"a": ["b"], "b": ["a"]}
    out = rank_step(links, {"a": 0.5, "b": 0.5})
    close(out, {"a": 0.5, "b": 0.5})


def test_hub_collects_score():
    links = {"hub": [], "x": ["hub"], "y": ["hub"]}
    ranks = {k: 1 / 3 for k in links}
    out = rank_step(links, ranks, damping=0.5)
    # base 1/6 each; x and y give 0.5*(1/3) to hub; hub spreads 0.5*(1/3)/3 to all
    expected_hub = 1 / 6 + 2 * (0.5 / 3) + (0.5 / 9)
    expected_x = 1 / 6 + 0.5 / 9
    close(out, {"hub": expected_hub, "x": expected_x, "y": expected_x})


def test_total_stays_one():
    links = {"a": ["b", "c"], "b": ["c"], "c": []}
    ranks = {k: 1 / 3 for k in links}
    assert sum(rank_step(links, ranks).values()) == pytest.approx(1.0)


def test_inputs_not_changed():
    links = {"a": ["b"], "b": []}
    ranks = {"a": 0.5, "b": 0.5}
    rank_step(links, ranks)
    assert ranks == {"a": 0.5, "b": 0.5}
    assert links == {"a": ["b"], "b": []}
