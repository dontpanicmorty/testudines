import pytest
from solution import render, refs_in


def test_simple():
    assert render("SELECT * FROM {{ ref('orders') }}", {"orders": "main.orders"}) == "SELECT * FROM main.orders"


def test_spacing_and_quotes():
    t = "{{ref('a')}} JOIN {{  ref( \"b\" )  }}"
    assert render(t, {"a": "A", "b": "B"}) == "A JOIN B"


def test_repeated():
    assert render("{{ ref('a') }}, {{ ref('a') }}", {"a": "x"}) == "x, x"


def test_no_refs_unchanged():
    assert render("SELECT 1", {}) == "SELECT 1"


def test_unknown_model():
    with pytest.raises(KeyError) as e:
        render("{{ ref('ghost') }}", {})
    assert "ghost" in str(e.value)


def test_refs_in():
    assert refs_in("{{ ref('a') }} {{ref(\"b\")}} {{ ref('a') }}") == ["a", "b"]
    assert refs_in("SELECT 1") == []
