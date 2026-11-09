def create_customer(store: dict[int, dict], body: dict) -> tuple[int, dict]:
    """Model POST /customers."""
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    if not name:
        return 422, {"error": "name is required"}
    if "@" not in email:
        return 422, {"error": "email must contain @"}
    for existing in store.values():
        if existing["email"] == email:
            return 409, {"error": "email already exists"}
    new_id = max(store, default=0) + 1
    customer = {"id": new_id, "name": name, "email": email}
    store[new_id] = customer
    return 201, customer
