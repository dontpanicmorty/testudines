def diff_schemas(old: dict[str, str], new: dict[str, str]) -> dict:
    raise NotImplementedError


def is_backward_compatible(old: dict[str, str], new: dict[str, str]) -> bool:
    raise NotImplementedError


def next_version(version: str, old: dict[str, str], new: dict[str, str]) -> str:
    raise NotImplementedError
