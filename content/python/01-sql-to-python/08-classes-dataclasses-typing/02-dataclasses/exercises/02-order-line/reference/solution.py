"""Order lines."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    order_id: int
    sku: str
    quantity: int
    unit_price_cents: int

    def __post_init__(self):
        sku = self.sku.strip().upper()
        if not sku:
            raise ValueError("sku must not be blank")
        if self.quantity < 1:
            raise ValueError(f"quantity must be at least 1, got {self.quantity}")
        if self.unit_price_cents < 0:
            raise ValueError(f"unit_price_cents must not be negative, got {self.unit_price_cents}")
        object.__setattr__(self, "sku", sku)

    @property
    def total_cents(self):
        return self.quantity * self.unit_price_cents
