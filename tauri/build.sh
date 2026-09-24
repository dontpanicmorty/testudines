#!/usr/bin/env bash
# Builds SQL Dojo.app (macOS) via Tauri. Cross-compiling a real Windows .exe/.msi from
# macOS isn't practical (Windows bundling needs NSIS/WiX, which don't run here) — for a
# Windows build, run `cargo tauri build` on a Windows machine with the Rust toolchain
# installed; ../webapp is the same, unmodified frontend either way.
#
# Bundles just the .app (--bundles app), skipping the .dmg step: DMG creation drives
# Finder via AppleScript to lay out the installer window/icons, which needs Automation
# permissions that aren't available in every environment (e.g. sandboxed/headless ones).
# If you want a .dmg for distribution, run `cargo tauri build` (no --bundles flag) from a
# normal Terminal session instead.
set -euo pipefail
cd "$(dirname "$0")/src-tauri"

if ! command -v cargo >/dev/null 2>&1; then
  echo "cargo not found — install Rust first: https://rustup.rs" >&2
  exit 1
fi
if ! cargo tauri --version >/dev/null 2>&1; then
  echo "Installing tauri-cli (one-time)..."
  cargo install tauri-cli --version "^2.0.0" --locked
fi

cargo tauri build --bundles app

echo
echo "Built: src-tauri/target/release/bundle/macos/SQL Dojo.app"
echo "Run with: open \"src-tauri/target/release/bundle/macos/SQL Dojo.app\""
