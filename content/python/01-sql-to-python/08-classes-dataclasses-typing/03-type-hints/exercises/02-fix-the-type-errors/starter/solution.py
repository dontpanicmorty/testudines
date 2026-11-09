"""Customer lookup helpers."""

CUSTOMERS: dict[str, dict[str, str]] = {
    "c1": {"name": "Ada", "email": "ada@example.com"},
    "c2": {"name": "Grace", "email": "grace@example.com"},
}


def find_email(customer_id: str) -> str:
    customer = CUSTOMERS.get(customer_id)
    return customer["email"]


def average_age(ages: list[int]) -> int:
    return sum(ages) / len(ages)


def total_rows(counts: list[str]) -> int:
    return sum(counts)
