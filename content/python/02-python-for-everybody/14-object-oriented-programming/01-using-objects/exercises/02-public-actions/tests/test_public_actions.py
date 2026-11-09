from solution import actions


def test_string_methods():
    result = actions("abc")
    assert "upper" in result and "split" in result
    assert result == sorted(result)


def test_list_methods():
    result = actions([])
    assert "append" in result and "sort" in result
    assert not any(n.startswith("_") for n in result)


def test_excludes_data_attributes():
    class Thing:
        size = 3

        def go(self):
            return 1

        def _hidden(self):
            return 2

    assert actions(Thing()) == ["go"]


def test_empty_for_plain_object():
    class Blank:
        pass

    assert actions(Blank()) == []
