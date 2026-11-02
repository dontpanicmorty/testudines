def get_order(orders: dict[int, dict], raw_id: str) -> tuple[int, dict]:
    """Model GET /orders/{id}. Return (status, body)."""
    try:
        order_id = int(raw_id)
    except (TypeError, ValueError):
        return 400, {"error": "invalid order id"}
    order = orders.get(order_id)
    if order is None:
        return 404, {"error": f"order {order_id} not found"}
    return 200, order
