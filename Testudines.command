#!/usr/bin/env bash
# Double-click launcher for macOS (runs run.sh next to this file).
exec "$(cd "$(dirname "$0")" && pwd)/run.sh" "$@"
