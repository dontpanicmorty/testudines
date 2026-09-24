#!/usr/bin/env bash
# Fully stops a SQL Dojo server started by start.sh, including an orphaned one
# left behind by closing its terminal window/tab directly.
set -uo pipefail
PORT="${1:-8765}"

PIDS=$(lsof -ti "tcp:${PORT}")
if [ -z "$PIDS" ]; then
  echo "Nothing is running on port ${PORT}."
  exit 0
fi

kill $PIDS 2>/dev/null
sleep 0.3
STILL=$(lsof -ti "tcp:${PORT}")
if [ -n "$STILL" ]; then
  kill -9 $STILL 2>/dev/null
fi

echo "Stopped SQL Dojo on port ${PORT}."
