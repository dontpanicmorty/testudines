Write `describe_params(params)` returning a one-line string safe to put in a log: `key=value` pairs sorted by key and joined with `", "`.

- Any key whose lower-cased name is in `SECRET_KEYS` (`password`, `private_key`, `token`, `passcode`) shows `***` instead of its value.
- Other keys show their value normally (so `private_key_file`, a path, stays visible).
- If a value is a dict (e.g. `session_parameters`), render it as `{k=v, k2=v2}` with keys sorted, applying the same redaction recursively.
- The input must not be modified.

```python
describe_params({"user": "SVC", "password": "hunter2", "role": "LOADER"})
# "password=***, role=LOADER, user=SVC"
```
