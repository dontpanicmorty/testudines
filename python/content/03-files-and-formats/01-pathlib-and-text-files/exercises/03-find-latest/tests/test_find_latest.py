from solution import latest_export


def touch(folder, *names):
    for n in names:
        (folder / n).write_text("x", encoding="utf-8")


def test_numeric_order(tmp_path):
    touch(tmp_path, "orders_9.csv", "orders_10.csv", "orders_2.csv")
    assert latest_export(tmp_path).name == "orders_10.csv"


def test_ignores_other_files(tmp_path):
    touch(tmp_path, "orders_3.csv", "orders_notes.txt", "orders_final.csv", "orders_4.csv.bak")
    assert latest_export(tmp_path).name == "orders_3.csv"


def test_empty(tmp_path):
    touch(tmp_path, "readme.txt")
    assert latest_export(tmp_path) is None
