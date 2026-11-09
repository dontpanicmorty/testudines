from solution import split_export


def test_basic():
    lines = ["ID, Name ,Plan", "1, Ada ,pro", "", "2,Grace,free"]
    assert split_export(lines) == (
        ["id", "name", "plan"],
        [("1", "Ada", "pro"), ("2", "Grace", "free")],
    )


def test_rows_are_tuples():
    _, rows = split_export(["a,b", "1,2"])
    assert isinstance(rows[0], tuple)


def test_header_only_and_whitespace_lines():
    assert split_export(["a,b", "   "]) == (["a", "b"], [])
