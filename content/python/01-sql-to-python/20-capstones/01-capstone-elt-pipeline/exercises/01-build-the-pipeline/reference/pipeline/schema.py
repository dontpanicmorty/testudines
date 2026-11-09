"""Row validation: split raw CSV rows into clean typed rows and quarantined rows."""
from datetime import datetime
from typing import Iterable

VALID_STATUSES = frozenset({"completed", "shipped", "cancelled", "refunded"})
TS_FORMAT = "%Y-%m-%d %H:%M:%S"


def _positive_int(value, field: str) -> int:
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be a positive integer")
    if number < 1:
        raise ValueError(f"{field} must be a positive integer")
    return number


def _text(value, field: str) -> str:
    text = (value or "").strip() if isinstance(value, str) or value is None else str(value).strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _split(rows: Iterable[dict], source: str, key: str, clean_one) -> tuple[list[dict], list[dict]]:
    good: list[dict] = []
    bad: list[dict] = []
    seen: set = set()
    for row in rows:
        try:
            clean = clean_one(row)
        except ValueError as exc:
            bad.append({"source": source, "reason": str(exc), "raw": dict(row)})
            continue
        if key and clean[key] in seen:
            bad.append({"source": source, "reason": f"duplicate {key}", "raw": dict(row)})
            continue
        if key:
            seen.add(clean[key])
        good.append(clean)
    return good, bad


def _clean_order(row: dict) -> dict:
    placed_at = _text(row.get("placed_at"), "placed_at")
    try:
        datetime.strptime(placed_at, TS_FORMAT)
    except ValueError:
        raise ValueError("placed_at must look like YYYY-MM-DD HH:MM:SS")
    status = _text(row.get("status"), "status").lower()
    if status not in VALID_STATUSES:
        raise ValueError(f"status {status!r} is not allowed")
    return {
        "order_id": _positive_int(row.get("order_id"), "order_id"),
        "customer_id": _positive_int(row.get("customer_id"), "customer_id"),
        "placed_at": placed_at,
        "status": status,
    }


def _clean_item(row: dict) -> dict:
    order_id = _positive_int(row.get("order_id"), "order_id")
    product_id = _text(row.get("product_id"), "product_id")
    quantity = _positive_int(row.get("quantity"), "quantity")
    try:
        unit_price = float(str(row.get("unit_price")).strip())
    except ValueError:
        raise ValueError("unit_price must be a number")
    if unit_price != unit_price or unit_price < 0:
        raise ValueError("unit_price must be a number >= 0")
    return {"order_id": order_id, "product_id": product_id, "quantity": quantity, "unit_price": unit_price}


def _clean_customer(row: dict) -> dict:
    return {
        "customer_id": _positive_int(row.get("customer_id"), "customer_id"),
        "region": _text(row.get("region"), "region").lower(),
    }


def validate_orders(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    return _split(rows, "orders", "order_id", _clean_order)


def validate_items(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    return _split(rows, "order_items", "", _clean_item)


def validate_customers(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    return _split(rows, "customers", "customer_id", _clean_customer)
