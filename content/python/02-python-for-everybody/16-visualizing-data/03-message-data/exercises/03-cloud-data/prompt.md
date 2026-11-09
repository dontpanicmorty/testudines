Write `cloud_json(subjects, top, stop_words)` that returns a JSON **string** for a word cloud.

- `subjects` is a list of text lines.
- Words are runs of letters and apostrophes (`[a-z']+`) after lowercasing the line.
- Words in `stop_words` (a set) are ignored.
- Count the remaining words across all lines, order them by count descending then word ascending, and keep the first `top`.
- Return `json.dumps` of a list of `{"text": word, "size": count}` objects.

```python
cloud_json(["Bird count rota", "bird rota"], 2, set())
# '[{"text": "bird", "size": 2}, {"text": "rota", "size": 2}]'
```
