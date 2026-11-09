import pytest

from solution import build_merge_sql


def norm(sql):
    return " ".join(sql.replace(";", " ").split()).upper()


def test_single_key():
    sql = build_merge_sql("orders", "orders_stg", ["order_id"], ["order_id", "status", "amount"])
    assert norm(sql) == norm(
        "MERGE INTO orders AS tgt USING orders_stg AS src ON tgt.order_id = src.order_id "
        "WHEN MATCHED THEN UPDATE SET tgt.status = src.status, tgt.amount = src.amount "
        "WHEN NOT MATCHED THEN INSERT (order_id, status, amount) VALUES (src.order_id, src.status, src.amount)"
    )


def test_composite_key():
    sql = norm(build_merge_sql("t", "s", ["a", "b"], ["a", "b", "v"]))
    assert "ON TGT.A = SRC.A AND TGT.B = SRC.B" in sql
    assert "UPDATE SET TGT.V = SRC.V WHEN NOT MATCHED" in sql


def test_all_columns_are_keys_omits_update():
    sql = norm(build_merge_sql("t", "s", ["a"], ["a"]))
    assert "WHEN MATCHED" not in sql
    assert "WHEN NOT MATCHED THEN INSERT (A) VALUES (SRC.A)" in sql


def test_no_semicolon():
    assert not build_merge_sql("t", "s", ["a"], ["a", "b"]).rstrip().endswith(";")


@pytest.mark.parametrize("keys,cols", [([], ["a"]), (["z"], ["a", "b"]), (["a"], [])])
def test_validation(keys, cols):
    with pytest.raises(ValueError):
        build_merge_sql("t", "s", keys, cols)
