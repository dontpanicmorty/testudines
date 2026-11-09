def flatten_event(event):
    user = event.get("user", {})
    return {
        "user_id": user.get("id"),
        "country": user.get("geo", {}).get("country"),
        "plan": event.get("props", {}).get("plan", "free"),
    }
