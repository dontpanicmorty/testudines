import sys
from importlib import metadata

from solution import describe_environment, installed_version


def test_keys():
    assert set(describe_environment()) == {"in_venv", "python", "has_site_packages"}


def test_values():
    d = describe_environment()
    assert d["in_venv"] is (sys.prefix != sys.base_prefix)
    assert d["python"] == f"{sys.version_info.major}.{sys.version_info.minor}"
    expected = any(p.endswith(("site-packages", "dist-packages")) for p in sys.path)
    assert d["has_site_packages"] is expected


def test_installed_version():
    assert installed_version("pytest") == metadata.version("pytest")


def test_missing_package_is_none():
    assert installed_version("definitely-not-installed-xyz") is None
