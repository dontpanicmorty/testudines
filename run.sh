#!/usr/bin/env bash
# Testudines launcher (macOS / Linux). Self-contained: uses no system Python.
# First run needs internet (fetches uv, Python, packages). Afterwards works offline.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
export UV_PYTHON_INSTALL_DIR="$HERE/.tools/python"
export UV_PYTHON_PREFERENCE=only-managed
export UV_PROJECT_ENVIRONMENT="$HERE/.venv"
export UV_CACHE_DIR="$HERE/.tools/uv-cache"
export UV_NO_ENV_FILE=1

if [ -x "$HERE/.tools/bin/uv" ]; then
  UV="$HERE/.tools/bin/uv"
elif command -v uv >/dev/null 2>&1; then
  UV="$(command -v uv)"
else
  echo "Installing uv into $HERE/.tools/bin (one-time)..."
  curl -LsSf https://astral.sh/uv/install.sh | UV_UNMANAGED_INSTALL="$HERE/.tools/bin" sh
  UV="$HERE/.tools/bin/uv"
fi

# Trust the OS certificate store (needed behind corporate TLS inspection). Newer uv calls this
# UV_SYSTEM_CERTS and warns about the old UV_NATIVE_TLS; older uv only knows UV_NATIVE_TLS.
unset UV_NATIVE_TLS UV_SYSTEM_CERTS VIRTUAL_ENV
case "$("$UV" help 2>/dev/null || true)" in
  *--system-certs*) export UV_SYSTEM_CERTS=1 ;;
  *) export UV_NATIVE_TLS=1 ;;
esac

exec "$UV" run testudines "$@"
