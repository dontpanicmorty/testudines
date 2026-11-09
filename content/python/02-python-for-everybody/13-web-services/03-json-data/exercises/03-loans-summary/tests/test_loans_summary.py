import json
from solution import summarize_loans


def test_example():
    text = json.dumps([
        {"member": "ines", "book": "Tide Tables", "days": 14},
        {"member": "omar", "book": "Moss and Stone", "days": 7},
        {"member": "ines", "book": "Reed Songs", "days": 21},
    ])
    assert summarize_loans(text) == '{"ines": 35, "omar": 7}'


def test_empty():
    assert summarize_loans("[]") == "{}"


def test_keys_sorted():
    text = json.dumps([{"member": m, "book": "x", "days": 1} for m in ("zed", "amy", "mo")])
    assert summarize_loans(text) == '{"amy": 1, "mo": 1, "zed": 1}'


def test_returns_text():
    assert isinstance(summarize_loans('[{"member": "a", "book": "b", "days": 2}]'), str)
