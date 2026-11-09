from solution import kind_names


def test_mixed():
    assert kind_names([1, "a", 2.5, None, [1]]) == ["int", "str", "float", "NoneType", "list"]


def test_empty():
    assert kind_names([]) == []


def test_containers_and_bool():
    assert kind_names([{}, (1,), True, {1}]) == ["dict", "tuple", "bool", "set"]
