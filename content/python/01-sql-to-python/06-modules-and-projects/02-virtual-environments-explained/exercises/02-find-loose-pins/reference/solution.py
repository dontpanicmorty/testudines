"""Requirements auditing."""
import re


def unpinned(text):
    """Return sorted lower-case names of requirements not pinned with ==."""
    names = set()
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        spec = line.split(";", 1)[0].strip()
        name = re.split(r"[\s\[<>=!~]", spec, maxsplit=1)[0].lower()
        if "==" not in spec:
            names.add(name)
    return sorted(names)
