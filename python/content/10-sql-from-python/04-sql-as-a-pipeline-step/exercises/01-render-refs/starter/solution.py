def render(template: str, relations: dict[str, str]) -> str:
    """Replace {{ ref('x') }} with relations['x']."""
    raise NotImplementedError


def refs_in(template: str) -> list[str]:
    """Referenced model names, first-appearance order, no duplicates."""
    raise NotImplementedError
