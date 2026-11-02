import json

import pytest
from typer.testing import CliRunner

from solution import app

runner = CliRunner()


def test_csv_default():
    r = runner.invoke(app, ["sample"])
    assert r.exit_code == 0, r.output
    assert r.stdout == "id,name\n1,user1\n2,user2\n3,user3\n"


def test_json_lines():
    r = runner.invoke(app, ["sample", "--count", "2", "--format", "json"])
    rows = [json.loads(line) for line in r.stdout.splitlines()]
    assert rows == [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]


@pytest.mark.parametrize("args", [["--format", "xml"], ["--count", "0"], ["--count", "-2"], ["--count", "x"]])
def test_invalid_input_rejected_with_code_2(args):
    r = runner.invoke(app, ["sample", *args])
    assert r.exit_code == 2, f"{args} gave exit {r.exit_code}; stdout={r.stdout!r}"
    assert r.stdout == ""


def test_version_still_works():
    assert runner.invoke(app, ["version"]).stdout == "1.0\n"
