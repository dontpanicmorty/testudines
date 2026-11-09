Write the loader for a JSONL event feed.

`load_events(lines, model, max_reject_rate=0.25)` takes an iterable of text lines and a pydantic model class. It returns `(valid, rejects)`:

- `valid`: model instances, in order.
- `rejects`: list of `{"line_no": n, "line": original_text, "reason": str}` where `line_no` is the 1-based line number in the input. `reason` starts with `"invalid json"` for undecodable text, is `"not an object"` for JSON that is not a dict, and starts with `"invalid fields"` (followed by `": "` and the comma-separated field names, sorted) for validation errors.
- Blank or whitespace-only lines are ignored (but still count for line numbers).

Define `class TooManyRejects(Exception)` and raise it, instead of returning, when `rejected / (valid + rejected)` is **strictly greater** than `max_reject_rate`. With no non-blank lines return `([], [])`.
