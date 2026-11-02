#!/usr/bin/env bash
# Builds a self-contained "Py Dojo.app" and a .dmg for macOS.
# The bundle embeds its own Python and every library: the result needs no
# internet, no uv, and no system Python. Building needs internet once.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"
DIST="$HERE/dist"
APP="$DIST/Py Dojo.app"
RES="$APP/Contents/Resources"
ARCH="$(uname -m)"
VERSION="$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml | head -1)"

# --- uv (build-time only) -------------------------------------------------
if [ -x "$HERE/.tools/bin/uv" ]; then UV="$HERE/.tools/bin/uv"
elif command -v uv >/dev/null 2>&1; then UV="$(command -v uv)"
else
  curl -LsSf https://astral.sh/uv/install.sh | UV_UNMANAGED_INSTALL="$HERE/.tools/bin" sh
  UV="$HERE/.tools/bin/uv"
fi
export UV_NO_ENV_FILE=1
export UV_NATIVE_TLS=1   # trust the OS certificate store (works behind corporate TLS inspection)

echo "==> Cleaning"
rm -rf "$APP" "$DIST/build-tmp"
mkdir -p "$APP/Contents/MacOS" "$RES" "$DIST/build-tmp"

echo "==> Embedding Python 3.12"
UV_PYTHON_INSTALL_DIR="$DIST/build-tmp/py" "$UV" python install 3.12
SRC_PY="$(cd "$(ls -d "$DIST"/build-tmp/py/cpython-3.12*-macos-* | head -1)" && pwd -P)"
cp -R "$SRC_PY" "$RES/python"
PY="$RES/python/bin/python3"
"$PY" --version

echo "==> Installing Py Dojo + libraries into the bundled Python"
"$UV" pip install --python "$PY" --break-system-packages --compile-bytecode "$HERE"

echo "==> Bundling lessons and datasets"
rsync -a --exclude '__pycache__' --exclude '.pytest_cache' --exclude '.ruff_cache' --exclude '.mypy_cache' \
  "$HERE/content/" "$RES/content/"
rsync -a --exclude '__pycache__' "$HERE/datasets/" "$RES/datasets/"

echo "==> Icon"
"$UV" run --quiet python scripts/make_icon.py >/dev/null
ICONSET="$DIST/build-tmp/PyDojo.iconset"
mkdir -p "$ICONSET"
SRC_ICON="$HERE/src/pydojo/assets/icon.png"
for s in 16 32 128 256 512; do
  sips -z $s $s "$SRC_ICON" --out "$ICONSET/icon_${s}x${s}.png" >/dev/null
  sips -z $((s*2)) $((s*2)) "$SRC_ICON" --out "$ICONSET/icon_${s}x${s}@2x.png" >/dev/null
done
iconutil -c icns "$ICONSET" -o "$RES/PyDojo.icns"

echo "==> Launcher + Info.plist"
cat > "$APP/Contents/MacOS/PyDojo" <<'LAUNCH'
#!/bin/bash
DIR="$(cd "$(dirname "$0")/.." && pwd)"
unset PYTHONHOME PYTHONPATH PYTHONSTARTUP VIRTUAL_ENV
export PYDOJO_PACKAGED=1
export PYTHONDONTWRITEBYTECODE=1
export PYDOJO_CONTENT="$DIR/Resources/content"
export PYDOJO_DATASETS="$DIR/Resources/datasets"
exec "$DIR/Resources/python/bin/python3" -m pydojo "$@"
LAUNCH
chmod +x "$APP/Contents/MacOS/PyDojo"
cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>CFBundleName</key><string>Py Dojo</string>
  <key>CFBundleDisplayName</key><string>Py Dojo</string>
  <key>CFBundleIdentifier</key><string>com.pydojo.app</string>
  <key>CFBundleVersion</key><string>${VERSION}</string>
  <key>CFBundleShortVersionString</key><string>${VERSION}</string>
  <key>CFBundleExecutable</key><string>PyDojo</string>
  <key>CFBundleIconFile</key><string>PyDojo</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
  <key>LSApplicationCategoryType</key><string>public.app-category.education</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>NSRequiresAquaSystemAppearance</key><false/>
</dict></plist>
PLIST

echo "==> Self-test of the packaged build"
PYDOJO_HOME="$DIST/build-tmp/selftest-data" QT_QPA_PLATFORM=offscreen "$APP/Contents/MacOS/PyDojo" selftest

echo "==> Ad-hoc signing"
find "$APP" -name '__pycache__' -prune -o -name '.DS_Store' -delete 2>/dev/null || true
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"
echo "==> Re-running self-test on the signed app; the seal must survive a run"
PYDOJO_HOME="$DIST/build-tmp/selftest-data2" QT_QPA_PLATFORM=offscreen "$APP/Contents/MacOS/PyDojo" selftest >/dev/null
codesign --verify --deep --strict "$APP" && echo "signature intact"

echo "==> Disk image"
DMG="$DIST/PyDojo-${VERSION}-${ARCH}.dmg"
rm -f "$DMG"
STAGE="$DIST/build-tmp/dmg"
mkdir -p "$STAGE"
cp -R "$APP" "$STAGE/"
ln -s /Applications "$STAGE/Applications"
hdiutil create -quiet -volname "Py Dojo" -srcfolder "$STAGE" -ov -format UDZO "$DMG"
rm -rf "$DIST/build-tmp"
echo
echo "Built:"
du -sh "$APP" "$DMG"
