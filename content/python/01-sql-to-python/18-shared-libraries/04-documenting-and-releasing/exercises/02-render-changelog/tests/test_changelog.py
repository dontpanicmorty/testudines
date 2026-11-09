from solution import render_changelog

EXPECTED = """## [1.5.0] - 2026-02-01

### Added
- top_n option.

### Fixed
- Trim spaces.

## [1.4.0] - 2026-01-10

### Added
- First release.
"""


def test_example_from_prompt():
    out = render_changelog([
        ("1.5.0", "2026-02-01", "Fixed", "Trim spaces."),
        ("1.5.0", "2026-02-01", "Added", "top_n option."),
        ("1.4.0", "2026-01-10", "Added", "First release."),
    ])
    assert out == EXPECTED


def test_empty():
    assert render_changelog([]) == ""


def test_kind_order_and_multiple_entries():
    out = render_changelog([
        ("2.0.0", "2026-03-01", "Removed", "read_rows."),
        ("2.0.0", "2026-03-01", "Changed", "Default strict."),
        ("2.0.0", "2026-03-01", "Added", "A."),
        ("2.0.0", "2026-03-01", "Added", "B."),
        ("2.0.0", "2026-03-01", "Deprecated", "old_thing."),
    ])
    assert out.index("### Added") < out.index("### Changed") < out.index("### Deprecated") < out.index("### Removed")
    assert "- A.\n- B." in out
    assert out.endswith("- read_rows.\n") and not out.endswith("\n\n")
