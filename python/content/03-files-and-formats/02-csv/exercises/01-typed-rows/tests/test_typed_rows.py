from solution import read_order_lines


def write(tmp_path, text):
    p = tmp_path / "lines.csv"
    p.write_text(text, encoding="utf-8")
    return p


def test_types_and_values(tmp_path):
    p = write(tmp_path, "order_id,product_id,quantity,unit_price\n1,P-7,3,4.5\n2,P-9,1,10\n")
    rows = read_order_lines(p)
    assert rows == [
        {"order_id": 1, "product_id": "P-7", "quantity": 3, "unit_price": 4.5},
        {"order_id": 2, "product_id": "P-9", "quantity": 1, "unit_price": 10.0},
    ]
    assert type(rows[0]["order_id"]) is int
    assert type(rows[1]["unit_price"]) is float


def test_empty_body(tmp_path):
    p = write(tmp_path, "order_id,product_id,quantity,unit_price\n")
    assert read_order_lines(p) == []
