from solution import write_parquet, read_parquet_rows

ROWS = [{"sku": "B", "qty": 5, "price": 2.5}, {"sku": "A", "qty": 1, "price": 10.0},
        {"sku": "C", "qty": 0, "price": 0.99}]


def test_roundtrip_and_creates_dirs(tmp_path):
    p = tmp_path / "nested" / "dir" / "x.parquet"
    assert write_parquet(ROWS, p) == 3
    assert p.exists()
    out = read_parquet_rows(p)
    assert out == sorted(ROWS, key=lambda r: r["sku"])


def test_min_qty_filter(tmp_path):
    p = str(tmp_path / "x.parquet")
    write_parquet(ROWS, p)
    assert [r["sku"] for r in read_parquet_rows(p, min_qty=1)] == ["A", "B"]
    assert [r["sku"] for r in read_parquet_rows(p, min_qty=6)] == []


def test_types_survive(tmp_path):
    p = tmp_path / "x.parquet"
    write_parquet(ROWS, p)
    r = read_parquet_rows(p)[0]
    assert isinstance(r["qty"], int) and isinstance(r["price"], float)
