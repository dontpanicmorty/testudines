from decimal import Decimal

from solution import read_valid

HEADER = "order_id,customer_id,sku,quantity,unit_price\n"


def write(tmp_path, body):
    p = tmp_path / "lines.csv"
    p.write_text(HEADER + body, encoding="utf-8")
    return p


def test_valid_rows_typed(tmp_path):
    valid, rejects = read_valid(write(tmp_path, "A1,1, x-100 ,2,5.00\n"))
    assert rejects == []
    assert valid == [
        {"order_id": "A1", "customer_id": 1, "sku": "X-100", "quantity": 2, "unit_price": Decimal("5.00")}
    ]
    assert type(valid[0]["unit_price"]) is Decimal


def test_rejects_have_line_numbers_and_all_reasons(tmp_path):
    body = "A1,1,x,2,5.00\nA2,two,y,0,5.00\nA3,3,z,1,abc\n,4,w,1,1\n"
    valid, rejects = read_valid(write(tmp_path, body))
    assert len(valid) == 1
    assert [r["line"] for r in rejects] == [3, 4, 5]
    assert "customer_id" in rejects[0]["reason"] and "quantity" in rejects[0]["reason"]
    assert "unit_price" in rejects[1]["reason"]
    assert "order_id" in rejects[2]["reason"]


def test_negative_price_and_blank_sku(tmp_path):
    valid, rejects = read_valid(write(tmp_path, "A1,1,,1,-1\n"))
    assert valid == []
    assert "sku" in rejects[0]["reason"] and "unit_price" in rejects[0]["reason"]


def test_counts_reconcile(tmp_path):
    body = "A1,1,x,1,1\nbad,x,x,x,x\nA2,2,y,2,2\n"
    valid, rejects = read_valid(write(tmp_path, body))
    assert len(valid) + len(rejects) == 3


def test_header_only(tmp_path):
    assert read_valid(write(tmp_path, "")) == ([], [])
