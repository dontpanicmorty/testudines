#!/usr/bin/env bash
# Launches SQL Dojo locally and opens it in your browser.
# A local server is required because browsers block ES-module imports (used to load
# the in-browser SQL engine, and the curriculum data file) from file:// pages.
set -uo pipefail
cd "$(dirname "$0")"
PORT="${1:-8765}"

# If a SQL Dojo server from an earlier session is still running on this port
# (e.g. its terminal window/tab was closed instead of stopped with Ctrl-C or
# ./stop.sh, orphaning the process), just reuse it instead of failing with
# "Address already in use".
if curl -s -o /dev/null --max-time 1 "http://localhost:${PORT}/index.html"; then
  echo "SQL Dojo is already running at http://localhost:${PORT} — reusing it."
  open "http://localhost:${PORT}"
  exit 0
fi

echo "Serving SQL Dojo at http://localhost:${PORT}"
echo "(To fully stop it later: ./stop.sh, or Ctrl-C in this terminal.)"
( sleep 1 && open "http://localhost:${PORT}" ) &
python3 server.py "${PORT}"
status=$?

if [ "$status" -ne 0 ]; then
  echo
  echo "Could not start the server on port ${PORT} (exit code ${status})."
  echo "Something other than SQL Dojo may already be using that port. Try:"
  echo "  ./stop.sh ${PORT}      # stop whatever is bound to it"
  echo "  ./start.sh $((PORT+1)) # or just use a different port"
fi
exit "$status"
