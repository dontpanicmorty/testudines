import tomllib


def summarize_pyproject(text):
    project = tomllib.loads(text).get("project", {})
    for field in ("name", "version"):
        if field not in project:
            raise ValueError(f"[project] is missing {field!r}")
    scripts = {}
    for cmd, spec in project.get("scripts", {}).items():
        if ":" not in spec:
            raise ValueError(f"bad entry point for {cmd!r}: {spec!r}")
        module, func = spec.split(":", 1)
        scripts[cmd] = (module, func)
    return {
        "name": project["name"],
        "version": project["version"],
        "dependencies": list(project.get("dependencies", [])),
        "extras": sorted(project.get("optional-dependencies", {})),
        "scripts": scripts,
    }
