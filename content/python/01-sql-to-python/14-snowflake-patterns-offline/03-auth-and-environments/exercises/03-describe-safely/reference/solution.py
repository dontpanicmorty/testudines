SECRET_KEYS = {"password", "private_key", "token", "passcode"}


def _render(params: dict) -> str:
    parts = []
    for key in sorted(params):
        value = params[key]
        if key.lower() in SECRET_KEYS:
            shown = "***"
        elif isinstance(value, dict):
            shown = "{" + _render(value) + "}"
        else:
            shown = value
        parts.append(f"{key}={shown}")
    return ", ".join(parts)


def describe_params(params: dict) -> str:
    return _render(params)
