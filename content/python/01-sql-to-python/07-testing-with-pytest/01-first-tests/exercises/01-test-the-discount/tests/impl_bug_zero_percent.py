"""A 0 percent discount returns 0 instead of the unchanged price."""


def apply_discount(price, percent):
    """Return price reduced by percent (0-100 inclusive), rounded to 2 decimals."""
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be between 0 and 100, got {percent}")
    if percent == 0:
        return 0
    return round(price * (1 - percent / 100), 2)
