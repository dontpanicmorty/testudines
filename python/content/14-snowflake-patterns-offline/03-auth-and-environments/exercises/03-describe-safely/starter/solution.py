SECRET_KEYS = {"password", "private_key", "token", "passcode"}


def describe_params(params: dict) -> str:
    return ", ".join(f"{k}={v}" for k, v in sorted(params.items()))
