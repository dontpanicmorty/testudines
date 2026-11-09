import inspect
from solution import parse_lines


def test_basic():
    assert list(parse_lines(["o1, 19.99", "", "# comment", "o2,5"])) == [("o1", 19.99), ("o2", 5.0)]


def test_is_generator():
    assert inspect.isgenerator(parse_lines(["a,1"])), "parse_lines should be a generator function"


def test_lazy():
    consumed = []

    def source():
        for line in ["a,1", "b,2", "c,3"]:
            consumed.append(line)
            yield line

    gen = parse_lines(source())
    assert next(gen) == ("a", 1.0)
    assert consumed == ["a,1"], f"read too much: {consumed}"
