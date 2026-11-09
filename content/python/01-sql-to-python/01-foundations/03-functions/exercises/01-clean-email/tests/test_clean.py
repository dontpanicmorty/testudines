from solution import clean_email


def test_basic():
    assert clean_email("  Ada@Example.COM ") == "ada@example.com"


def test_blank_and_none():
    assert clean_email("   ") is None
    assert clean_email("") is None
    assert clean_email(None) is None


def test_docstring():
    assert clean_email.__doc__ and clean_email.__doc__.strip(), "add a docstring"
