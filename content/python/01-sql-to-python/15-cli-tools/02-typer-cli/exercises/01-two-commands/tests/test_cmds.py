from typer.testing import CliRunner

from solution import app

runner = CliRunner()


def test_greet():
    r = runner.invoke(app, ["greet", "Ada"])
    assert r.exit_code == 0, r.output
    assert r.stdout == "Hello, Ada!\n"


def test_greet_upper():
    assert runner.invoke(app, ["greet", "Ada", "--upper"]).stdout == "HELLO, ADA!\n"


def test_repeat_default_and_times():
    assert runner.invoke(app, ["repeat", "hi"]).stdout == "hi\nhi\n"
    assert runner.invoke(app, ["repeat", "hi", "--times", "3"]).stdout == "hi\nhi\nhi\n"


def test_bad_times_is_usage_error():
    assert runner.invoke(app, ["repeat", "hi", "--times", "x"]).exit_code == 2
