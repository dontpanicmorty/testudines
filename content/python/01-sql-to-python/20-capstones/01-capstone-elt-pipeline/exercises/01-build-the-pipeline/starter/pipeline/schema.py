"""Row validation: split raw CSV rows into clean typed rows and quarantined rows.

Every validate_* function takes an iterable of raw dict rows (all values are text, as
csv.DictReader gives them) and returns (good_rows, quarantined_rows).

A quarantined row is {"source": <name>, "reason": <text naming the field>, "raw": <the original row>}.
"""
from typing import Iterable

VALID_STATUSES = frozenset({"completed", "shipped", "cancelled", "refunded"})
TS_FORMAT = "%Y-%m-%d %H:%M:%S"


def validate_orders(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    """source name: "orders". Clean row keys: order_id, customer_id (ints), placed_at (str), status (lowercase)."""
    raise NotImplementedError


def validate_items(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    """source name: "order_items". Clean keys: order_id, quantity (ints), product_id (str), unit_price (float)."""
    raise NotImplementedError


def validate_customers(rows: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    """source name: "customers". Clean keys: customer_id (int), region (lowercase str)."""
    raise NotImplementedError
