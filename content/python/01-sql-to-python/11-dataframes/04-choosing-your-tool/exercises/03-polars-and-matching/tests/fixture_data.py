ORDERS = [
    {"order_id": 1, "customer_id": 10, "status": "shipped"},
    {"order_id": 2, "customer_id": 20, "status": "cancelled"},
    {"order_id": 3, "customer_id": 20, "status": "completed"},
    {"order_id": 4, "customer_id": 30, "status": "completed"},
    {"order_id": 5, "customer_id": 40, "status": "completed"},
    {"order_id": 6, "customer_id": 50, "status": "cancelled"},
    {"order_id": 7, "customer_id": 10, "status": "completed"},
]
ITEMS = [
    {"order_id": 1, "quantity": 2, "unit_price": 10.0},
    {"order_id": 2, "quantity": 9, "unit_price": 99.0},
    {"order_id": 3, "quantity": 1, "unit_price": 25.0},
    {"order_id": 3, "quantity": 1, "unit_price": 5.0},
    {"order_id": 4, "quantity": 3, "unit_price": 10.0},
    {"order_id": 5, "quantity": 1, "unit_price": 29.99},
    {"order_id": 6, "quantity": 4, "unit_price": 4.0},
    {"order_id": 7, "quantity": 1, "unit_price": 0.1},
    {"order_id": 7, "quantity": 1, "unit_price": 0.2},
]
# 30 -> 30.0 ; 20 -> 30.0 (tie, lower id first) ; 40 -> 29.99 ; 10 -> 20.3 ; 50 cancelled
EXPECTED = [(20, 30.0), (30, 30.0), (40, 29.99), (10, 20.3)]
