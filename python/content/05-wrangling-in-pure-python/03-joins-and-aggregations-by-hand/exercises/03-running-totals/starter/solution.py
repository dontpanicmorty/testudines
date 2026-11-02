"""add_window_columns(orders) -> list[dict]

Sort by (customer, day), then add running_total (per customer) and
prev_amount (LAG, None for the first row of each customer). Do not mutate input.
"""
