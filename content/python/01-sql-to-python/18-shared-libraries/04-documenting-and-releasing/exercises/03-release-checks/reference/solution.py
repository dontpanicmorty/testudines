import re
import tomllib
from pathlib import Path


def check_release(project_dir):
    root = Path(project_dir)
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return ["no_version"]
    project = tomllib.loads(pyproject.read_text()).get("project", {})
    if "version" not in project or "name" not in project:
        return ["no_version"]
    version = project["version"]
    problems = []
    if not (root / "README.md").exists():
        problems.append("missing_readme")
    changelog = root / "CHANGELOG.md"
    if not changelog.exists():
        problems.append("missing_changelog")
    elif not re.search(rf"^## \[{re.escape(version)}\]", changelog.read_text(), re.M):
        problems.append("changelog_version")
    init = root / "src" / project["name"].replace("-", "_") / "__init__.py"
    found = None
    if init.exists():
        m = re.search(r"""__version__\s*=\s*["']([^"']+)["']""", init.read_text())
        found = m.group(1) if m else None
    if found != version:
        problems.append("version_mismatch")
    return problems
