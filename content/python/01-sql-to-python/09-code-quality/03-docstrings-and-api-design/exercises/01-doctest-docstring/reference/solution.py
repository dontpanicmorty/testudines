"""Duration parsing."""

import re

SECONDS = {"d": 86400, "h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    """Convert a compact duration such as ``"1h30m"`` into seconds.

    Args:
        text: One or more ``<digits><unit>`` parts, with units ``d``, ``h``,
            ``m`` and ``s``. Surrounding whitespace is ignored.

    Returns:
        The total number of seconds.

    Raises:
        ValueError: If ``text`` is not a valid duration.

    Examples:
        >>> parse_duration("1h30m")
        5400
        >>> parse_duration(" 45s ")
        45
        >>> parse_duration("2d")
        172800
    """
    body = text.strip()
    if not re.fullmatch(r"(\d+[dhms])+", body):
        raise ValueError(f"not a duration: {text!r}")
    return sum(int(n) * SECONDS[u] for n, u in re.findall(r"(\d+)([dhms])", body))
