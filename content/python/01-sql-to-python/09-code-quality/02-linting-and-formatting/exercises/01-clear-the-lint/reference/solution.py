import json

names: list[str] = []


def read_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def has_key(config, key):
    return config is not None and config.get(key) is not None


def add_name(name):
    names.append(name)
