"""Order lookups."""
from customers import get_customer

ORDERS = [(100, 1), (101, 1), (102, 2)]


def orders_for(customer_id):
    return [oid for oid, cid in ORDERS if cid == customer_id]


def describe_order(order_id):
    for oid, cid in ORDERS:
        if oid == order_id:
            return f"order {oid} for {get_customer(cid)}"
    raise KeyError(order_id)
