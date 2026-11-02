import copy

from solution import redact


def test_flat():
    assert redact({"user": "svc", "Password": "p", "API_TOKEN": "t"}) == {
        "user": "svc", "Password": "***", "API_TOKEN": "***"}


def test_nested_dict():
    got = redact({"opts": {"private_key": "k", "region": "eu"}})
    assert got == {"opts": {"private_key": "***", "region": "eu"}}, f"nested secret leaked: {got}"


def test_lists_of_dicts():
    got = redact({"conns": [{"name": "a", "secret": "x"}, {"name": "b", "secret": "y"}]})
    assert got == {"conns": [{"name": "a", "secret": "***"}, {"name": "b", "secret": "***"}]}


def test_input_not_mutated():
    data = {"a": {"token": "t"}, "b": [{"password": "p"}]}
    snapshot = copy.deepcopy(data)
    redact(data)
    assert data == snapshot


def test_headers_authorization():
    assert redact({"headers": {"Authorization": "Bearer abc", "Accept": "json"}}) == {
        "headers": {"Authorization": "***", "Accept": "json"}}


def test_non_secret_values_untouched():
    assert redact({"n": 3, "flag": None, "tags": ["a", "b"]}) == {"n": 3, "flag": None, "tags": ["a", "b"]}
