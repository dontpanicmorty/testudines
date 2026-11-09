import json


def dig(json_text, path, default=None):
    value = json.loads(json_text)
    for key in path:
        try:
            value = value[key]
        except (KeyError, IndexError, TypeError):
            return default
    return value
