import re

REF = re.compile(r"""\{\{\s*ref\(\s*(['"])([^'"]+)\1\s*\)\s*\}\}""")


def render(template: str, relations: dict[str, str]) -> str:
    """Replace {{ ref('x') }} with relations['x']."""
    def replace(match: re.Match) -> str:
        name = match.group(2)
        if name not in relations:
            raise KeyError(f"unknown model {name!r}")
        return relations[name]

    return REF.sub(replace, template)


def refs_in(template: str) -> list[str]:
    """Referenced model names, first-appearance order, no duplicates."""
    return list(dict.fromkeys(m.group(2) for m in REF.finditer(template)))
