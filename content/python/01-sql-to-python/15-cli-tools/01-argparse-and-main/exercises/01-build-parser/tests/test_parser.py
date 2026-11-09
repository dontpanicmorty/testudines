import pytest

from solution import build_parser


def test_defaults():
    a = build_parser().parse_args(["orders.csv"])
    assert (a.input, a.output, a.limit, a.env, a.dry_run) == ("orders.csv", "-", None, "dev", False)


def test_all_options():
    a = build_parser().parse_args(["o.csv", "-o", "out.csv", "--limit", "10", "--env", "prod", "--dry-run"])
    assert (a.input, a.output, a.limit, a.env, a.dry_run) == ("o.csv", "out.csv", 10, "prod", True)


def test_long_output():
    assert build_parser().parse_args(["x", "--output", "y"]).output == "y"


@pytest.mark.parametrize("argv", [["x", "--limit", "abc"], ["x", "--env", "staging"], []])
def test_invalid_exits_2(argv):
    with pytest.raises(SystemExit) as info:
        build_parser().parse_args(argv)
    assert info.value.code == 2
