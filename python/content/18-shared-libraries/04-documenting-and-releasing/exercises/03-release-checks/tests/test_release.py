from solution import check_release


def make(tmp_path, *, version="1.5.0", init_version="1.5.0", readme=True,
         changelog="## [Unreleased]\n\n## [1.5.0] - 2026-02-01\n- x\n"):
    (tmp_path / "pyproject.toml").write_text(
        f'[project]\nname = "acme-datakit"\nversion = "{version}"\n'
    )
    pkg = tmp_path / "src" / "acme_datakit"
    pkg.mkdir(parents=True)
    body = f'__version__ = "{init_version}"\n' if init_version else "X = 1\n"
    (pkg / "__init__.py").write_text(body)
    if readme:
        (tmp_path / "README.md").write_text("# datakit\n")
    if changelog is not None:
        (tmp_path / "CHANGELOG.md").write_text(changelog)
    return tmp_path


def test_clean(tmp_path):
    assert check_release(make(tmp_path)) == []


def test_missing_files(tmp_path):
    assert check_release(make(tmp_path, readme=False, changelog=None)) == [
        "missing_readme", "missing_changelog"]


def test_changelog_lacks_version(tmp_path):
    p = make(tmp_path, changelog="## [1.4.0] - 2026-01-01\n")
    assert check_release(p) == ["changelog_version"]


def test_changelog_prefix_not_confused(tmp_path):
    p = make(tmp_path, changelog="## [1.5.01] - 2026-01-01\n")
    assert check_release(p) == ["changelog_version"]


def test_version_mismatch(tmp_path):
    assert check_release(make(tmp_path, init_version="1.4.9")) == ["version_mismatch"]


def test_missing_dunder_version(tmp_path):
    assert check_release(make(tmp_path, init_version=None)) == ["version_mismatch"]


def test_multiple_in_order(tmp_path):
    p = make(tmp_path, readme=False, init_version="0.0.1", changelog="nothing\n")
    assert check_release(p) == ["missing_readme", "changelog_version", "version_mismatch"]


def test_no_pyproject(tmp_path):
    assert check_release(tmp_path) == ["no_version"]
    (tmp_path / "pyproject.toml").write_text("[tool.x]\na = 1\n")
    assert check_release(tmp_path) == ["no_version"]
