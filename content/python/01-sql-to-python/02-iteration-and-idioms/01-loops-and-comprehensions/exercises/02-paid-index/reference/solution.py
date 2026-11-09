def index_paid(orders):
    return {o["order_id"]: o["amount"] for o in orders if o["status"].strip().lower() == "paid"}


def line_numbers(lines):
    return [f"{i}: {line}" for i, line in enumerate(lines, start=1)]
