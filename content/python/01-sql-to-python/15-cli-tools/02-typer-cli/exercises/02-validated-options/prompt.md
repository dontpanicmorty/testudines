`sample --count N --format csv|json` prints `N` demo rows (ids 1..N). Currently `--format xml` and `--count 0` are happily accepted, and a typo silently produces CSV.

Make the command reject bad input with Typer's own validation (exit code `2`, nothing printed to stdout):

- `--count` (default 3) must be at least 1;
- `--format` (default `csv`) must be exactly `csv` or `json`.

Output: for `csv`, a header line `id,name` then `1,user1`, `2,user2`...; for `json`, one JSON object per line like `{"id": 1, "name": "user1"}`.

A second command `version` (prints `1.0`) is provided so `sample` stays a named subcommand.
