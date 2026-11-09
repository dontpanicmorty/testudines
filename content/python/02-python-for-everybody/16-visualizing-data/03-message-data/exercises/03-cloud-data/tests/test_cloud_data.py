import json

from solution import cloud_json


def test_example():
    out = cloud_json(["Bird count rota", "bird rota"], 2, set())
    assert out == '[{"text": "bird", "size": 2}, {"text": "rota", "size": 2}]'


def test_stop_words_removed():
    out = json.loads(cloud_json(["the Heron and the Wren", "The heron"], 5, {"the", "and"}))
    assert out == [{"text": "heron", "size": 2}, {"text": "wren", "size": 1}]


def test_top_limits_and_ties_alphabetical():
    out = json.loads(cloud_json(["delta alpha charlie bravo"], 3, set()))
    assert [w["text"] for w in out] == ["alpha", "bravo", "charlie"]


def test_apostrophes_kept_and_empty():
    assert json.loads(cloud_json(["Don't stop"], 5, set()))[0] == {"text": "don't", "size": 1}
    assert cloud_json([], 3, set()) == "[]"


def test_numbers_and_punctuation_ignored():
    out = json.loads(cloud_json(["Rota #42: spring!"], 5, set()))
    assert [w["text"] for w in out] == ["rota", "spring"]
