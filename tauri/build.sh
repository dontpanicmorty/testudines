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
  echo "cargo not found. SQL Dojo needs the Rust toolchain to build." >&2
  read -r -p 'Type "agree" to install Rust now via rustup (https://rustup.rs). Any other submission will abort the Rust installation and app setup: ' reply
  if [ "$reply" = "agree" ]; then
    # --no-modify-path: some setups have a root-owned/unwritable shell profile
    # (e.g. ~/.bash_profile from a managed install) that rustup can't safely
    # amend. This build script only needs `cargo` on PATH for the rest of this
    # run, which `source "$HOME/.cargo/env"` below already provides — it
    # doesn't need rustup to touch any shell startup file.
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
    # shellcheck disable=SC1090
    source "$HOME/.cargo/env"
  else
    echo "Aborting: Rust installation and app setup were not agreed to." >&2
    exit 1
  fi
fi
if ! cargo tauri --version >/dev/null 2>&1; then
  echo "Installing tauri-cli (one-time)..."
  cargo install tauri-cli --version "^2.0.0" --locked
fi

cargo tauri build --bundles app

echo
echo "Built: src-tauri/target/release/bundle/macos/SQL Dojo.app"
echo "Run with: open \"src-tauri/target/release/bundle/macos/SQL Dojo.app\""
