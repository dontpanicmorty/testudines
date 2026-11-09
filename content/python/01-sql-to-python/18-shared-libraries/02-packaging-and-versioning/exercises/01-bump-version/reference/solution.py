def _parse(version):
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"not a MAJOR.MINOR.PATCH version: {version!r}")
    return tuple(int(p) for p in parts)


def bump(version, part):
    major, minor, patch = _parse(version)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unknown part: {part!r}")


def is_newer(a, b):
    return _parse(a) > _parse(b)
