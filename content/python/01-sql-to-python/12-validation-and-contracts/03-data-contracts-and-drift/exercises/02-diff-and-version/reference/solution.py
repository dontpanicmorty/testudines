def diff_schemas(old: dict[str, str], new: dict[str, str]) -> dict:
    common = sorted(old.keys() & new.keys())
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "retyped": {c: (old[c], new[c]) for c in common if old[c] != new[c]},
    }


def is_backward_compatible(old: dict[str, str], new: dict[str, str]) -> bool:
    diff = diff_schemas(old, new)
    if diff["removed"]:
        return False
    return all(pair == ("int", "float") for pair in diff["retyped"].values())


def next_version(version: str, old: dict[str, str], new: dict[str, str]) -> str:
    major, minor, _patch = (int(p) for p in version.split("."))
    if not is_backward_compatible(old, new):
        return f"{major + 1}.0.0"
    diff = diff_schemas(old, new)
    if diff["added"] or diff["retyped"]:
        return f"{major}.{minor + 1}.0"
    return version
