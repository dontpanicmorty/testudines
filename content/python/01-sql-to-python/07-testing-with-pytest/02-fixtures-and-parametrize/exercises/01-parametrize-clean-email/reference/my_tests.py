import pytest

from emails import clean_email


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("ada@example.com", "ada@example.com"),
        ("ADA@Example.COM", "ada@example.com"),
        ("  ada@example.com  ", "ada@example.com"),
        (None, None),
        ("", None),
        ("   ", None),
        ("no-at-sign", None),
        ("a@@b.com", None),
        ("a@b@c.com", None),
        ("@example.com", None),
        ("ada@", None),
    ],
)
def test_clean_email(raw, expected):
    assert clean_email(raw) == expected
