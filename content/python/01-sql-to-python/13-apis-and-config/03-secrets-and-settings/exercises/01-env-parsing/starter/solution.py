from collections.abc import Mapping


class ConfigError(Exception):
    pass


def parse_bool(text: str) -> bool:
    return bool(text)


def get_int(env: Mapping[str, str], name: str, default: int) -> int:
    return int(env[name])
