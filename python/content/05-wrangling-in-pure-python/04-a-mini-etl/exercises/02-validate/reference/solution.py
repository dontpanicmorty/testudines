import csv
from decimal import Decimal, InvalidOperation


def _validate(raw):
    errors = []
    order_id = (raw.get("order_id") or "").strip()
    if not order_id:
        errors.append("order_id is required")
    sku = (raw.get("sku") or "").strip().upper()
    if not sku:
        errors.append("sku is required")
    customer_id = None
    try:
        customer_id = int((raw.get("customer_id") or "").strip())
    except ValueError:
        errors.append("customer_id must be an integer")
    quantity = None
    try:
        quantity = int((raw.get("quantity") or "").strip())
        if quantity <= 0:
            errors.append("quantity must be positive")
    except ValueError:
        errors.append("quantity must be an integer")
    unit_price = None
    try:
        unit_price = Decimal((raw.get("unit_price") or "").strip())
        if not unit_price.is_finite() or unit_price < 0:
            errors.append("unit_price must be a non-negative number")
    except InvalidOperation:
        errors.append("unit_price must be a number")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "sku": sku,
        "quantity": quantity,
        "unit_price": unit_price,
    }


def read_valid(path):
    valid, rejects = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, raw in enumerate(csv.DictReader(f), start=2):
            try:
                valid.append(_validate(raw))
            except ValueError as e:
                rejects.append({"line": line_no, "reason": str(e)})
    return valid, rejects
