"""Pure transformation: validated rows in, daily revenue rows out. No I/O here."""

REVENUE_STATUSES = frozenset({"completed", "shipped"})


def daily_revenue(orders: list[dict], items: list[dict], customers: list[dict]) -> list[dict]:
    """Return rows {"day", "region", "orders", "revenue"} sorted by (day, region)."""
    raise NotImplementedError
