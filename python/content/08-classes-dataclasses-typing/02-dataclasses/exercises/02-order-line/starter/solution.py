"""Order lines."""
from dataclasses import dataclass


@dataclass
class OrderLine:
    order_id: int
    sku: str
    quantity: int
    unit_price_cents: int
