import zipfile

from solution import build_wheel


def make_pkg(root):
    pkg = root / "src" / "acme_datakit"
    (pkg / "sub").mkdir(parents=True)
    # newline="\n": the same file bytes on every system (Windows would otherwise write "\r\n")
    (pkg / "__init__.py").write_text("X = 1\n", newline="\n")
    (pkg / "core.py").write_text("def f(): return 1\n", newline="\n")
    (pkg / "sub" / "__init__.py").write_text("")
    (pkg / "sub" / "deep.py").write_text("Y = 2\n", newline="\n")
    (pkg / "data.txt").write_text("not python")
    (pkg / "__pycache__").mkdir()
    (pkg / "__pycache__" / "core.cpython-312.py").write_text("junk")
    return pkg


def test_name_and_return(tmp_path):
    pkg = make_pkg(tmp_path)
    wheel = build_wheel(pkg, "acme-datakit", "1.4.2", tmp_path / "dist")
    assert wheel.name == "acme_datakit-1.4.2-py3-none-any.whl"
    assert wheel.exists()
    assert zipfile.is_zipfile(wheel)


def test_contents(tmp_path):
    pkg = make_pkg(tmp_path)
    wheel = build_wheel(pkg, "acme-datakit", "1.4.2", tmp_path / "dist")
    with zipfile.ZipFile(wheel) as zf:
        names = sorted(zf.namelist())
    assert names == [
        "acme_datakit-1.4.2.dist-info/METADATA",
        "acme_datakit/__init__.py",
        "acme_datakit/core.py",
        "acme_datakit/sub/__init__.py",
        "acme_datakit/sub/deep.py",
    ]


def test_metadata_and_file_content(tmp_path):
    pkg = make_pkg(tmp_path)
    wheel = build_wheel(pkg, "acme-datakit", "1.4.2", tmp_path / "dist")
    with zipfile.ZipFile(wheel) as zf:
        meta = zf.read("acme_datakit-1.4.2.dist-info/METADATA").decode()
        assert meta == "Metadata-Version: 2.1\nName: acme-datakit\nVersion: 1.4.2\n"
        assert zf.read("acme_datakit/core.py").decode() == "def f(): return 1\n"
