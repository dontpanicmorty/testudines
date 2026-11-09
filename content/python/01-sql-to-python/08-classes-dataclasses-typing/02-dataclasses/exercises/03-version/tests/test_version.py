import pytest

from solution import Version


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1", Version(1, 0, 0)),
        ("1.2", Version(1, 2, 0)),
        ("1.2.3", Version(1, 2, 3)),
        ("v1.2.3", Version(1, 2, 3)),
        ("v2", Version(2, 0, 0)),
        ("10.20.30", Version(10, 20, 30)),
    ],
)
def test_parse(text, expected):
    assert Version.parse(text) == expected


@pytest.mark.parametrize("bad", ["", "v", "1.x", "1.2.3.4", "a.b", "1..2", "-1.0"])
def test_parse_rejects(bad):
    with pytest.raises(ValueError):
        Version.parse(bad)


def test_str_has_three_parts():
    assert str(Version(1, 2)) == "1.2.0"
    assert str(Version.parse("v2.1")) == "2.1.0"


def test_sorts_numerically():
    versions = [Version.parse(t) for t in ["1.10", "1.9.1", "1", "1.9", "0.99.99"]]
    assert [str(v) for v in sorted(versions)] == ["0.99.99", "1.0.0", "1.9.0", "1.9.1", "1.10.0"]


def test_comparison_and_immutability():
    assert Version(1, 10) > Version(1, 9)
    assert len({Version(1, 2), Version(1, 2, 0)}) == 1
    with pytest.raises(AttributeError):
        Version(1).major = 2
