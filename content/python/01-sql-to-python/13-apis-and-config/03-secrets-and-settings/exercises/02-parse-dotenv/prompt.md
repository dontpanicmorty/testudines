Write `parse_dotenv(text)` that turns the contents of a `.env` file into a `dict[str, str]`.

Rules:

- Blank lines and lines starting with `#` are ignored.
- Each other line is `KEY=VALUE`. Split on the **first** `=` only. Whitespace around the key and value is stripped.
- An optional leading `export ` is allowed before the key.
- A value wrapped in matching single or double quotes has the quotes removed (inside the quotes, whitespace is kept).
- A later duplicate key overrides an earlier one.
- A non-blank, non-comment line without `=` raises `ValueError` whose message contains `line N` (1-based).

```python
parse_dotenv('A=1\n# note\nexport B = "x y"\nTOKEN=abc==')
# {"A": "1", "B": "x y", "TOKEN": "abc=="}
```
