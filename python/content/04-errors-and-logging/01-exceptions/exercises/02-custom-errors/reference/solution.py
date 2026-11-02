class RowError(Exception):
    def __init__(self, row_number, message):
        self.row_number = row_number
        super().__init__(f"row {row_number}: {message}")


def parse_row(row, row_number):
    id_raw, amount_raw = row["id"], row["amount"]
    try:
        id_ = int(id_raw)
    except ValueError as e:
        raise RowError(row_number, f"invalid id {id_raw!r}") from e
    try:
        amount = float(amount_raw)
    except ValueError as e:
        raise RowError(row_number, f"invalid amount {amount_raw!r}") from e
    return {"id": id_, "amount": amount}
