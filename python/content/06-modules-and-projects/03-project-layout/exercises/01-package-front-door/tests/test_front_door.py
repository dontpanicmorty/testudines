def test_reexports():
    from mylib import clean_name, read_rows

    assert clean_name("  ada   lovelace ") == "Ada Lovelace"
    assert read_rows("a,b\n1,2\n") == [{"a": "1", "b": "2"}]


def test_version():
    import mylib

    assert mylib.__version__ == "0.1.0"


def test_all():
    import mylib

    assert sorted(mylib.__all__) == ["clean_name", "read_rows"]


def test_same_objects():
    import mylib
    from mylib.cleaning import clean_name

    assert mylib.clean_name is clean_name
