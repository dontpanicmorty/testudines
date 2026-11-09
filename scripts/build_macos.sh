#!/usr/bin/env bash
# Builds a self-contained "Testudines.app" and a .dmg for macOS.
# The bundle embeds its own Python and every library: the result needs no
# internet, no uv, and no system Python. Building needs internet once.
#
#   scripts/build_macos.sh                      this Mac's kind: Apple silicon (arm64) or Intel (x86_64)
#   TESTUDINES_ARCH=x86_64 scripts/build_macos.sh   an Intel build on an Apple silicon Mac (needs Rosetta,
#                                                   which runs its self-test)
#   TESTUDINES_ARCH=arm64 scripts/build_macos.sh    an Apple silicon build (only on an Apple silicon Mac)
#
# A build for this Mac's kind goes to dist/Testudines.app; another kind goes to dist/<arch>/Testudines.app.
# Either way the disk image is dist/Testudines-<version>-<arch>.dmg.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"
DIST="$HERE/dist"
HOST_ARCH="$(uname -m)"
ARCH="${TESTUDINES_ARCH:-$HOST_ARCH}"
case "$ARCH" in
  arm64) PY_ARCH=aarch64 ;;
  x86_64) PY_ARCH=x86_64 ;;
  *) echo "TESTUDINES_ARCH must be arm64 or x86_64, not $ARCH" >&2; exit 1 ;;
esac
if [ "$ARCH" != "$HOST_ARCH" ]; then
  [ "$HOST_ARCH" = arm64 ] && [ "$ARCH" = x86_64 ] || { echo "An $ARCH build needs an $ARCH Mac" >&2; exit 1; }
  arch -x86_64 /usr/bin/true 2>/dev/null || { echo "An Intel build on this Mac needs Rosetta: softwareupdate --install-rosetta" >&2; exit 1; }
  APP="$DIST/$ARCH/Testudines.app"
else
  APP="$DIST/Testudines.app"
fi
RES="$APP/Contents/Resources"
TMP="$DIST/build-tmp-$ARCH"
VERSION="$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml | head -1)"

# --- uv (build-time only) -------------------------------------------------
if [ -x "$HERE/.tools/bin/uv" ]; then UV="$HERE/.tools/bin/uv"
elif command -v uv >/dev/null 2>&1; then UV="$(command -v uv)"
else
  curl -LsSf https://astral.sh/uv/install.sh | UV_UNMANAGED_INSTALL="$HERE/.tools/bin" sh
  UV="$HERE/.tools/bin/uv"
fi
export UV_NO_ENV_FILE=1
# Trust the OS certificate store (needed behind corporate TLS inspection). Newer uv calls this
# UV_SYSTEM_CERTS and warns about the old UV_NATIVE_TLS; older uv only knows UV_NATIVE_TLS.
unset UV_NATIVE_TLS UV_SYSTEM_CERTS VIRTUAL_ENV
case "$("$UV" help 2>/dev/null || true)" in
  *--system-certs*) export UV_SYSTEM_CERTS=1 ;;
  *) export UV_NATIVE_TLS=1 ;;
esac

echo "==> Cleaning"
rm -rf "$APP" "$TMP"
mkdir -p "$APP/Contents/MacOS" "$RES" "$TMP"

echo "==> Embedding Python 3.12 ($ARCH)"
UV_PYTHON_INSTALL_DIR="$TMP/py" "$UV" python install "cpython-3.12-macos-$PY_ARCH-none"
SRC_PY="$(cd "$(ls -d "$TMP"/py/cpython-3.12*-macos-"$PY_ARCH"-* | head -1)" && pwd -P)"
cp -R "$SRC_PY" "$RES/python"
PY="$RES/python/bin/python3"
"$PY" --version
"$PY" -c "import platform; m = platform.machine(); assert m == '$ARCH', m; print('architecture', m)"

echo "==> Installing Testudines + libraries into the bundled Python"
"$UV" pip install --python "$PY" --break-system-packages --compile-bytecode "$HERE"
if [ "$ARCH" = x86_64 ]; then
  # Polars' default runtime needs AVX2-era CPU features that older Intel Macs (and Rosetta) lack;
  # its compatibility runtime runs on any 64-bit Intel CPU. The exercises' data is small, so speed is the same.
  echo "==> Polars compatibility runtime (any Intel CPU)"
  POLARS_VERSION="$("$PY" -c "import importlib.metadata as m; print(m.version('polars'))")"
  "$UV" pip install --python "$PY" --break-system-packages --compile-bytecode "polars-runtime-compat==$POLARS_VERSION"
  "$UV" pip uninstall --python "$PY" --break-system-packages polars-runtime-32 polars-runtime-64 2>/dev/null || true
fi

echo "==> Removing the parts of Qt the app never uses"
"$PY" -I "$HERE/scripts/prune_bundle.py" "$("$PY" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"

echo "==> Bundling the SQL and Python curricula and datasets"
rsync -a --exclude '__pycache__' --exclude '.pytest_cache' --exclude '.ruff_cache' --exclude '.mypy_cache' \
  "$HERE/content/" "$RES/content/"
rsync -a --exclude '__pycache__' "$HERE/datasets/" "$RES/datasets/"

echo "==> Icon"
ICONSET="$TMP/Testudines.iconset"
mkdir -p "$ICONSET"
SRC_ICON="$HERE/src/testudines/assets/icon.png"
for s in 16 32 128 256 512; do
  sips -z $s $s "$SRC_ICON" --out "$ICONSET/icon_${s}x${s}.png" >/dev/null
  sips -z $((s*2)) $((s*2)) "$SRC_ICON" --out "$ICONSET/icon_${s}x${s}@2x.png" >/dev/null
done
iconutil -c icns "$ICONSET" -o "$RES/Testudines.icns"

echo "==> Launcher + Info.plist"
cat > "$APP/Contents/MacOS/Testudines" <<'LAUNCH'
#!/bin/bash
DIR="$(cd "$(dirname "$0")/.." && pwd)"
unset PYTHONHOME PYTHONPATH PYTHONSTARTUP VIRTUAL_ENV
export TESTUDINES_PACKAGED=1
export PYTHONDONTWRITEBYTECODE=1
export TESTUDINES_CONTENT="$DIR/Resources/content"
export TESTUDINES_DATASETS="$DIR/Resources/datasets"
exec "$DIR/Resources/python/bin/python3" -m testudines "$@"
LAUNCH
chmod +x "$APP/Contents/MacOS/Testudines"
cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>CFBundleName</key><string>Testudines</string>
  <key>CFBundleDisplayName</key><string>Testudines</string>
  <key>CFBundleIdentifier</key><string>com.mauriceallen.testudines</string>
  <key>CFBundleVersion</key><string>${VERSION}</string>
  <key>CFBundleShortVersionString</key><string>${VERSION}</string>
  <key>CFBundleExecutable</key><string>Testudines</string>
  <key>CFBundleIconFile</key><string>Testudines</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>LSMinimumSystemVersion</key><string>14.0</string>
  <key>LSApplicationCategoryType</key><string>public.app-category.education</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>NSRequiresAquaSystemAppearance</key><false/>
</dict></plist>
PLIST

echo "==> Self-test of the packaged build"
TESTUDINES_HOME="$TMP/selftest-data" QT_QPA_PLATFORM=offscreen "$APP/Contents/MacOS/Testudines" selftest

echo "==> Ad-hoc signing"
find "$APP" -name '__pycache__' -prune -o -name '.DS_Store' -delete 2>/dev/null || true
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"
echo "==> Re-running self-test on the signed app; the seal must survive a run"
TESTUDINES_HOME="$TMP/selftest-data2" QT_QPA_PLATFORM=offscreen "$APP/Contents/MacOS/Testudines" selftest >/dev/null
codesign --verify --deep --strict "$APP" && echo "signature intact"
# The app is rebuilt at the same path, often while the old one is open: tell macOS it changed,
# so Finder and the Dock show its icon instead of a cached blank one.
touch "$APP"
LSREGISTER=/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister
[ -x "$LSREGISTER" ] && [ "$ARCH" = "$HOST_ARCH" ] && "$LSREGISTER" -f "$APP" || true

echo "==> Disk image"
DMG="$DIST/Testudines-${VERSION}-${ARCH}.dmg"
rm -f "$DMG"
STAGE="$TMP/dmg"
mkdir -p "$STAGE"
cp -R "$APP" "$STAGE/"
ln -s /Applications "$STAGE/Applications"
# hdiutil fails now and then with "Resource busy" (often on CI machines), so try a few times
for attempt in 1 2 3 4 5; do
  if hdiutil create -volname "Testudines" -srcfolder "$STAGE" -ov -format UDZO "$DMG"; then break; fi
  [ "$attempt" = 5 ] && { echo "Creating the disk image failed 5 times" >&2; exit 1; }
  echo "Disk image attempt $attempt failed; retrying in 10 seconds"
  sleep 10
done
rm -rf "$TMP"
echo
echo "Built:"
du -sh "$APP" "$DMG"
