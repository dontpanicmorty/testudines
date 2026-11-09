"""A percent above 100 is accepted instead of raising ValueError."""


def apply_discount(price, percent):
    """Return price reduced by percent (0-100 inclusive), rounded to 2 decimals."""
    if percent < 0:
        raise ValueError(f"percent must be between 0 and 100, got {percent}")
    return round(price * (1 - percent / 100), 2)
