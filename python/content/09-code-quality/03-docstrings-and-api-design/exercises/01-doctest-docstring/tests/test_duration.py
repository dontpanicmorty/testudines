import doctest

import pytest

import solution
from solution import parse_duration


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1h30m", 5400),
        ("45s", 45),
        ("2d", 172800),
        ("90s", 90),
        (" 5m ", 300),
        ("1d1h1m1s", 90061),
        ("10m10m", 1200),
    ],
)
def test_values(text, expected):
    assert parse_duration(text) == expected


@pytest.mark.parametrize("bad", ["", "   ", "abc", "10", "5x", "h", "1h 30m", "-5s", "1.5h"])
def test_invalid(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)


def test_docstring_sections():
    doc = parse_duration.__doc__ or ""
    first = doc.strip().splitlines()[0]
    assert first and first.endswith("."), "Start with a one-line summary sentence."
    for section in ("Args:", "Returns:", "Raises:", "Examples:"):
        assert section in doc, f"Add a '{section}' section to the docstring."
    assert "ValueError" in doc


def test_doctests_run_and_pass():
    result = doctest.testmod(solution)
    assert result.attempted >= 3, f"Write at least 3 doctest examples (found {result.attempted})."
    assert result.failed == 0, "One of your doctest examples gives a different output than written."
