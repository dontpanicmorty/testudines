import pytest
from typer.testing import CliRunner

from solution import app, summarize_csv

runner = CliRunner()


def write(tmp_path, text):
    f = tmp_path / "d.csv"
    f.write_text(text)
    return f


def test_happy_path(tmp_path):
    f = write(tmp_path, "id,amount\n1,10.25\n2,\n3,50.25\n")
    r = runner.invoke(app, ["summarize", str(f)])
    assert r.exit_code == 0, r.output
    assert r.stdout == "rows=3\nsum=60.50\n"


def test_other_column(tmp_path):
    f = write(tmp_path, "id,qty\n1,2\n2,3\n")
    assert runner.invoke(app, ["summarize", str(f), "--column", "qty"]).stdout == "rows=2\nsum=5.00\n"


def test_missing_file(tmp_path):
    r = runner.invoke(app, ["summarize", str(tmp_path / "nope.csv")])
    assert r.exit_code == 1 and r.stdout == ""
    assert r.stderr.startswith("error:")


def test_missing_column_named(tmp_path):
    f = write(tmp_path, "id,amount\n1,1\n")
    r = runner.invoke(app, ["summarize", str(f), "--column", "price"])
    assert r.exit_code == 1 and r.stdout == "" and "price" in r.stderr


def test_non_numeric_value(tmp_path):
    f = write(tmp_path, "id,amount\n1,abc\n")
    r = runner.invoke(app, ["summarize", str(f)])
    assert r.exit_code == 1 and r.stdout == "" and r.stderr.startswith("error:")


def test_plain_function(tmp_path):
    f = write(tmp_path, "amount\n1.5\n2.5\n")
    assert summarize_csv(f, "amount") == (2, 4.0)
    with pytest.raises(ValueError):
        summarize_csv(f, "nope")
    with pytest.raises(FileNotFoundError):
        summarize_csv(tmp_path / "x.csv", "amount")
