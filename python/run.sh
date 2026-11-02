#!/usr/bin/env bash
# Py Dojo launcher (macOS / Linux). Self-contained: uses no system Python.
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

exec "$UV" run pydojo "$@"
