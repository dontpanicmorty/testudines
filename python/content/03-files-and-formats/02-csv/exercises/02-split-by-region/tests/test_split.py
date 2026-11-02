import csv

from solution import split_by_region

SRC = (
    "customer_id,name,region,plan\n"
    "1,\"Smith, Jane\",EU,pro\n"
    "2,Bo,US,free\n"
    "3,Cy,EU,team\n"
)


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        return list(r)


def test_split(tmp_path):
    src = tmp_path / "customers.csv"
    src.write_text(SRC, encoding="utf-8")
    out = tmp_path / "out" / "nested"
    counts = split_by_region(src, out)
    assert counts == {"EU": 2, "US": 1}
    assert read(out / "EU.csv") == [
        ["customer_id", "name", "region", "plan"],
        ["1", "Smith, Jane", "EU", "pro"],
        ["3", "Cy", "EU", "team"],
    ]
    assert read(out / "US.csv") == [
        ["customer_id", "name", "region", "plan"],
        ["2", "Bo", "US", "free"],
    ]


def test_no_extra_files(tmp_path):
    src = tmp_path / "c.csv"
    src.write_text(SRC, encoding="utf-8")
    out = tmp_path / "o"
    split_by_region(src, out)
    assert sorted(p.name for p in out.iterdir()) == ["EU.csv", "US.csv"]
