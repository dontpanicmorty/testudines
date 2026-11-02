SENSITIVE = ("password", "secret", "token", "key", "authorization")


def redact(data):
    result = {}
    for k, v in data.items():
        if any(word in k.lower() for word in SENSITIVE):
            result[k] = "***"
        else:
            result[k] = v
    return result
