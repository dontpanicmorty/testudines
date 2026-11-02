class ValidationError(ValueError):
    pass


PLANS = {"free", "pro", "team"}


def validate_customer(raw):
    errors = []
    cid = None
    try:
        cid = int(str(raw.get("customer_id", "")).strip())
        if cid <= 0:
            errors.append("customer_id must be positive")
    except ValueError:
        errors.append("customer_id must be an integer")
    email = str(raw.get("email") or "").strip().lower()
    if email.count("@") != 1:
        errors.append("email must contain exactly one @")
    plan = str(raw.get("plan") or "").strip().lower()
    if plan not in PLANS:
        errors.append(f"plan must be one of {sorted(PLANS)}")
    if errors:
        raise ValidationError("; ".join(errors))
    return {"customer_id": cid, "email": email, "plan": plan}
