from solution import file_kind


def test_python():
    assert file_kind("script.py") == "python"


def test_case_ignored():
    assert file_kind("Notes.MD") == "text"


def test_table():
    assert file_kind("sales.2025.csv") == "table"


def test_unknown_and_no_extension():
    assert file_kind("archive.zip") == "unknown"
    assert file_kind("py") == "unknown"
