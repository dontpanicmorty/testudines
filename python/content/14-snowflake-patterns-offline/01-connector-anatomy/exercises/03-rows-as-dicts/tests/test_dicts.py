from solution import rows_as_dicts


class Cur:
    def __init__(self, names, rows):
        self.description = None if names is None else [(n, None, None, None, None, None, None) for n in names]
        self._rows = rows

    def fetchall(self):
        return list(self._rows)


def test_rows_are_distinct_dicts():
    cur = Cur(["ORDER_ID", "STATUS"], [(1, "open"), (2, "shipped"), (3, "open")])
    got = rows_as_dicts(cur)
    assert got == [
        {"order_id": 1, "status": "open"},
        {"order_id": 2, "status": "shipped"},
        {"order_id": 3, "status": "open"},
    ], f"got {got}"
    assert len({id(d) for d in got}) == 3


def test_no_result_set():
    assert rows_as_dicts(Cur(None, [])) == []


def test_empty_result_with_columns():
    assert rows_as_dicts(Cur(["A"], [])) == []


def test_names_lowercased():
    assert rows_as_dicts(Cur(["Customer_ID"], [(7,)])) == [{"customer_id": 7}]
