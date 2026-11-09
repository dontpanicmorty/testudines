import pytest

from solution import summarize_pyproject

FULL = """
[project]
name = "acme-datakit"
version = "1.4.2"
dependencies = ["pydantic>=2,<3"]

[project.optional-dependencies]
pandas = ["pandas>=2"]
dev = ["pytest"]

[project.scripts]
datakit = "acme_datakit.cli:main"
other = "acme_datakit.tools:run"
"""


def test_full():
    assert summarize_pyproject(FULL) == {
        "name": "acme-datakit",
        "version": "1.4.2",
        "dependencies": ["pydantic>=2,<3"],
        "extras": ["dev", "pandas"],
        "scripts": {
            "datakit": ("acme_datakit.cli", "main"),
            "other": ("acme_datakit.tools", "run"),
        },
    }


def test_minimal_defaults():
    out = summarize_pyproject('[project]\nname = "x"\nversion = "0.1.0"\n')
    assert out == {"name": "x", "version": "0.1.0", "dependencies": [],
                   "extras": [], "scripts": {}}


def test_missing_version():
    with pytest.raises(ValueError):
        summarize_pyproject('[project]\nname = "x"\n')


def test_missing_project_table():
    with pytest.raises(ValueError):
        summarize_pyproject('[tool.ruff]\nline-length = 100\n')


def test_bad_entry_point():
    text = '[project]\nname = "x"\nversion = "1.0.0"\n[project.scripts]\ncmd = "no_colon_here"\n'
    with pytest.raises(ValueError):
        summarize_pyproject(text)
