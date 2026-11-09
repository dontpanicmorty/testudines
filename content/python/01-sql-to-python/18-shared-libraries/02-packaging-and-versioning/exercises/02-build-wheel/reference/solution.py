import zipfile
from pathlib import Path


def build_wheel(package_dir, dist_name, version, out_dir):
    package_dir = Path(package_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    import_name = dist_name.replace("-", "_")
    wheel = out_dir / f"{import_name}-{version}-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(package_dir.rglob("*.py")):
            if "__pycache__" in f.parts:
                continue
            rel = f.relative_to(package_dir.parent).as_posix()
            zf.write(f, rel)
        zf.writestr(
            f"{import_name}-{version}.dist-info/METADATA",
            f"Metadata-Version: 2.1\nName: {dist_name}\nVersion: {version}\n",
        )
    return wheel
