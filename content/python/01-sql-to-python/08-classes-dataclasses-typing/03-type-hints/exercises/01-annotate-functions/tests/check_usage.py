from solution import first_or_none, group_by_region, total_cents

a: int = total_cents([1.5, 2.5])
b: str | None = first_or_none(["x"])
c: int | None = first_or_none([1, 2])
d: dict[str, list[str]] = group_by_region([{"region": "EU", "customer_id": "1"}])
