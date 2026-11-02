def create_customer(store: dict[int, dict], body: dict) -> tuple[int, dict]:
    """Model POST /customers."""
    name = body.get("name")
    email = body.get("email", "")
    if not name:
        return 422, {"error": "name is required"}
    for existing in store.values():
        if existing["email"] == email:
            return 409, {"error": "email already exists"}
    new_id = len(store) + 1
    customer = {"id": new_id, "name": name, "email": email}
    store[new_id] = customer
    return 200, customer
