from solution import first_failure


def test_value_error():
    assert first_failure(["1", "2", "x", "4"], int) == (
        2, "ValueError", "invalid literal for int() with base 10: 'x'"
    )


def test_all_ok():
    assert first_failure(["1", "2"], int) is None
    assert first_failure([], int) is None


def test_stops_at_first_and_other_types():
    seen = []

    def parse(row):
        seen.append(row)
        return {"a": 1}[row]

    assert first_failure(["a", "b", "a"], parse) == (1, "KeyError", "'b'")
    assert seen == ["a", "b"], f"parse called on rows after the failure: {seen}"
