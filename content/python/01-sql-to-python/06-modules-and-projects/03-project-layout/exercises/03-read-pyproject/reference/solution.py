"""Read project metadata from pyproject.toml text."""
import re
import tomllib


def project_info(text):
    data = tomllib.loads(text)
    if "project" not in data:
        raise ValueError("missing [project] table")
    project = data["project"]
    deps = [
        re.split(r"[\s\[<>=!~;]", d, maxsplit=1)[0].lower()
        for d in project.get("dependencies", [])
    ]
    scripts = {}
    for command, target in project.get("scripts", {}).items():
        module, _, func = target.partition(":")
        scripts[command] = (module, func)
    return {
        "name": project["name"],
        "version": project["version"],
        "dependencies": deps,
        "scripts": scripts,
    }
