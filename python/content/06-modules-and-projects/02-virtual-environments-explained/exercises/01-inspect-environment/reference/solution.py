"""Environment report helpers."""
import sys
from importlib import metadata


def describe_environment():
    return {
        "in_venv": sys.prefix != sys.base_prefix,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "has_site_packages": any(
            p.endswith(("site-packages", "dist-packages")) for p in sys.path
        ),
    }


def installed_version(package):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None
