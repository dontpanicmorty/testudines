"""Returns the discount amount instead of the discounted price."""


def apply_discount(price, percent):
    """Return price reduced by percent (0-100 inclusive), rounded to 2 decimals."""
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be between 0 and 100, got {percent}")
    return round(price * percent / 100, 2)
