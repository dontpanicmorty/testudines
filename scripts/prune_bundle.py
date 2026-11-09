"""Removes the parts of Qt (PySide6) that Testudines never uses from a built app's bundled Python.

Testudines uses only QtCore, QtGui and QtWidgets. PySide6 also ships Qt's QML/Quick stack, Designer,
Linguist, Assistant, translations, developer tools and headers: about 150-200 MB the app never loads.

    python scripts/prune_bundle.py <site-packages folder of the bundled Python>

macOS: keeps exactly the Qt frameworks that QtCore/QtGui/QtWidgets and the kept plugins link to (found
with otool), and removes the rest. Windows: removes the unused Qt families by name. Both build scripts
run the app's selftest after this, which opens every page, so a missing library fails the build.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

KEEP_MODULES = {"QtCore", "QtGui", "QtWidgets"}  # the PySide6 modules the app imports
KEEP_PLUGINS = {"platforms", "styles", "imageformats", "iconengines", "generic"}
DROP_IMAGE_PLUGINS = re.compile(r"qpdf", re.I)  # the PDF image plugin pulls in QtPdf and Qt Quick
# Windows: Qt families the app never loads (each has a Qt6<Name>*.dll)
WINDOWS_DROP = re.compile(r"^Qt6(Quick|Qml|Labs|Designer|Pdf|VirtualKeyboard|Lottie|Test|UiTools|Help|Sql|"
                          r"ShaderTools|Concurrent|OpenGLWidgets|SvgWidgets|PrintSupport|Xml|StateMachine)",
                          re.I)


def _remove(p: Path, freed: list[int]) -> None:
    if not p.exists() and not p.is_symlink():
        return
    if p.is_dir() and not p.is_symlink():
        freed[0] += sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())
        shutil.rmtree(p)
    else:
        freed[0] += p.stat().st_size if p.is_file() else 0
        p.unlink()


def _macos_needed(ps: Path, qt: Path) -> set[str]:
    """Qt framework names (e.g. 'QtGui') linked, directly or not, by the kept modules and plugins."""
    def links(binary: Path) -> set[str]:
        out = subprocess.run(["otool", "-L", str(binary)], capture_output=True, text=True).stdout
        return set(re.findall(r"(Qt\w+)\.framework", out))

    roots = [ps / f"{m}.abi3.so" for m in KEEP_MODULES] + list(ps.glob("libpyside6.abi3.*.dylib"))
    for d in KEEP_PLUGINS:
        roots += [f for f in (qt / "plugins" / d).glob("*.dylib") if not DROP_IMAGE_PLUGINS.search(f.name)]
    need: set[str] = set()
    for r in roots:
        need |= links(r)
    todo = set(need)
    while todo:
        name = todo.pop()
        binary = qt / "lib" / f"{name}.framework" / "Versions" / "A" / name
        for dep in links(binary) - need:
            need.add(dep)
            todo.add(dep)
    return need


def prune(site: Path) -> int:
    ps = site / "PySide6"
    if not ps.is_dir():
        raise SystemExit(f"no PySide6 in {site}")
    freed = [0]
    windows = (ps / "Qt6Core.dll").exists()
    qt = ps if windows else ps / "Qt"

    # developer tools, Qt Designer/Linguist/Assistant, headers and bindings data
    for p in ps.iterdir():
        if p.suffix == ".app" or p.suffix == ".exe" or (p.is_file() and not p.suffix and p.name != "py.typed"):
            _remove(p, freed)
    for name in ("include", "typesystems", "glue", "doc", "scripts", "support/generate_pyi.py"):
        _remove(ps / name, freed)
    for name in ("qml", "translations", "metatypes", "libexec", "resources"):
        _remove(qt / name, freed)
    # plugins: keep only what a desktop widgets app uses
    plugins = qt / "plugins"
    if plugins.is_dir():
        for d in plugins.iterdir():
            if d.name not in KEEP_PLUGINS:
                _remove(d, freed)
        for f in (plugins / "imageformats").glob("*"):
            if DROP_IMAGE_PLUGINS.search(f.name):
                _remove(f, freed)
    # Python bindings for modules the app never imports
    for f in ps.glob("Qt*.*"):
        module = f.name.split(".")[0]
        if module.startswith("Qt") and module not in KEEP_MODULES and f.suffix in (".so", ".pyd", ".pyi"):
            _remove(f, freed)
    for f in ps.glob("libpyside6qml*"):
        _remove(f, freed)
    for f in ps.glob("pyside6qml*.dll"):
        _remove(f, freed)
    # the Qt libraries themselves
    if windows:
        for f in ps.glob("Qt6*.dll"):
            if WINDOWS_DROP.match(f.name):
                _remove(f, freed)
        _remove(ps / "opengl32sw.dll", freed)  # software OpenGL; widgets draw without OpenGL
    else:
        need = _macos_needed(ps, qt)
        for fw in (qt / "lib").glob("*.framework"):
            if fw.name.removesuffix(".framework") not in need:
                _remove(fw, freed)
    print(f"pruned Qt: freed {freed[0] / 1e6:.0f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(prune(Path(sys.argv[1])))
