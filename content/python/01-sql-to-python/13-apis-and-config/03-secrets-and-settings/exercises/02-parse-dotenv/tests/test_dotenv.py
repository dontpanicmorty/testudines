import pytest

from solution import parse_dotenv


def test_basic_and_comments():
    assert parse_dotenv("A=1\n\n# c\nB=two") == {"A": "1", "B": "two"}


def test_first_equals_only():
    assert parse_dotenv("TOKEN=abc==") == {"TOKEN": "abc=="}


def test_quotes_and_spacing():
    got = parse_dotenv('A = "x  y"\nB=\'q\'\nC=  plain  ')
    assert got == {"A": "x  y", "B": "q", "C": "plain"}


def test_export_prefix():
    assert parse_dotenv("export REGION=eu") == {"REGION": "eu"}


def test_duplicate_last_wins():
    assert parse_dotenv("A=1\nA=2") == {"A": "2"}


def test_empty_value():
    assert parse_dotenv("A=") == {"A": ""}


def test_bad_line_reports_number():
    with pytest.raises(ValueError, match="line 3"):
        parse_dotenv("A=1\n# ok\noops\nB=2")


def test_unbalanced_quote_left_alone():
    assert parse_dotenv('A="oops') == {"A": '"oops'}
