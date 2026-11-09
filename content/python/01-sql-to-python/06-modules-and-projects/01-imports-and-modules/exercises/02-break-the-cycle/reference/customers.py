"""Customer lookups."""

CUSTOMERS = {1: "Ada", 2: "Grace"}


def get_customer(customer_id):
    return CUSTOMERS[customer_id]


def order_count(customer_id):
    from orders import orders_for

    return len(orders_for(customer_id))
