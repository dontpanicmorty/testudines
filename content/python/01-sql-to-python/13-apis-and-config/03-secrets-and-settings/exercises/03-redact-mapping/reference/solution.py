SENSITIVE = ("password", "secret", "token", "key", "authorization")


def redact(data):
    if isinstance(data, dict):
        out = {}
        for k, v in data.items():
            if isinstance(k, str) and any(word in k.lower() for word in SENSITIVE):
                out[k] = "***"
            else:
                out[k] = redact(v)
        return out
    if isinstance(data, list):
        return [redact(v) for v in data]
    if isinstance(data, tuple):
        return tuple(redact(v) for v in data)
    return data
