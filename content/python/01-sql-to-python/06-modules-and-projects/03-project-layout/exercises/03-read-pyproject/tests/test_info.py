import pytest

from solution import project_info

FULL = """
[project]
name = "mylib"
version = "0.1.0"
dependencies = ["Pandas>=2.0", "httpx[http2]>=0.27", 'numpy==1.26 ; python_version < "3.13"', "duckdb"]

[project.scripts]
ingest = "mylib.cli:main"
check = "mylib.checks:run_all"

[tool.ruff]
line-length = 100
"""


def test_full():
    info = project_info(FULL)
    assert info["name"] == "mylib"
    assert info["version"] == "0.1.0"
    assert info["dependencies"] == ["pandas", "httpx", "numpy", "duckdb"]
    assert info["scripts"] == {
        "ingest": ("mylib.cli", "main"),
        "check": ("mylib.checks", "run_all"),
    }


def test_minimal():
    info = project_info('[project]\nname = "x"\nversion = "1.0"\n')
    assert info == {"name": "x", "version": "1.0", "dependencies": [], "scripts": {}}


def test_missing_project_table():
    with pytest.raises(ValueError, match="missing .project. table"):
        project_info('[tool.ruff]\nline-length = 100\n')
