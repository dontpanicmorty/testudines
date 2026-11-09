+++
id = "files-and-formats.json-and-jsonl"
title = "JSON and JSONL"
minutes = 30
+++

# JSON and JSONL

APIs, event streams, dbt artifacts and Snowflake `VARIANT` columns are all JSON. You already navigate it in SQL with `payload:user.id::int` and `LATERAL FLATTEN`. In Python JSON becomes ordinary dicts and lists, which you navigate with square brackets.

> **SQL bridge.** `payload:user:plan::string` → `payload["user"]["plan"]`. A missing path in Snowflake gives `NULL`; in Python a missing key raises `KeyError` unless you use `.get`.

## Loading and dumping

```python
import json

text = '{"id": 7, "tags": ["a", "b"], "meta": {"ok": true, "note": null}}'
obj = json.loads(text)             # str -> Python
print(obj["meta"]["ok"], obj["meta"]["note"], obj["tags"][0])
print(json.dumps(obj, indent=2, sort_keys=True))
```

The mapping: object ↔ `dict`, array ↔ `list`, string ↔ `str`, number ↔ `int`/`float`, `true/false` ↔ `True/False`, `null` ↔ `None`.

`loads`/`dumps` work on strings; `load`/`dump` work on open files:

```python
import json
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "cfg.json"
    with p.open("w", encoding="utf-8") as f:
        json.dump({"retries": 3, "name": "Zoë"}, f, ensure_ascii=False)
    with p.open(encoding="utf-8") as f:
        print(json.load(f))
```

JSON has no dates, no `Decimal`, no sets. `json.dumps({"d": datetime.date(2025, 1, 1)})` raises `TypeError: Object of type date is not JSON serializable`. Convert to strings first (or pass `default=str` as a last resort).

## Safe navigation

> **Predict first.** Which line raises?

```python
# no-run
event = {"user": {"id": 5}, "props": None}
print(event.get("user", {}).get("id"))      # 5
print(event.get("missing", {}).get("x"))    # None
print(event["props"].get("path"))           # raises
```

The third raises `AttributeError: 'NoneType' object has no attribute 'get'`: the key exists but holds `null`. The `.get(k, {})` chain only protects against *missing* keys. The robust version uses `or {}`:

```python
event = {"user": {"id": 5}, "props": None}
path = (event.get("props") or {}).get("path")
print(path)
```

For a reusable helper, write one function and test it once:

```python
def dig(obj, *keys, default=None):
    """Walk nested dicts/lists; return default if any step is missing."""
    for k in keys:
        try:
            obj = obj[k]
        except (KeyError, IndexError, TypeError):
            return default
    return obj

doc = {"a": {"b": [10, 20]}}
print(dig(doc, "a", "b", 1), dig(doc, "a", "x", 1, default="n/a"))
```

## JSON Lines (JSONL)

A JSON document must be parsed whole. **JSONL** puts one JSON object per line, so you can stream it, append to it and split it. Event logs and bulk loads use it constantly.

```python
import json

lines = [
    '{"event_id": "e1", "user": {"id": 1}}',
    '{"event_id": "e2", "user": {"id": 2}}',
]
for line in lines:
    ev = json.loads(line)
    print(ev["event_id"], ev["user"]["id"])
```

Real files contain damage: truncated writes, stray log text. One bad line should not kill a million good ones. Catch the specific error and **count** what you skipped:

```python
import json

lines = ['{"a": 1}', '{"a": 2', "", "not json", '{"a": 3}']
good, bad = [], 0
for n, line in enumerate(lines, start=1):
    if not line.strip():
        continue
    try:
        good.append(json.loads(line))
    except json.JSONDecodeError as e:
        bad += 1
        print(f"line {n}: {e.msg}")
print(len(good), "good,", bad, "bad")
```

Writing JSONL is `f.write(json.dumps(obj) + "\n")` per record, with no indentation (one line per object).

## Walking a dbt-style manifest

A dbt `manifest.json` has a `nodes` dict keyed by `unique_id`, and each node lists upstream ids under `depends_on.nodes`. That is a graph stored as a dict, and you can walk it with a small recursive function.

```python
manifest = {
    "nodes": {
        "model.shop.stg_orders": {"depends_on": {"nodes": ["source.shop.raw.orders"]}},
        "model.shop.int_totals": {"depends_on": {"nodes": ["model.shop.stg_orders"]}},
        "model.shop.fct_sales": {"depends_on": {"nodes": ["model.shop.int_totals", "model.shop.stg_orders"]}},
    },
}

def upstream(manifest, node_id, seen=None):
    """All ancestors of node_id (sources included)."""
    seen = set() if seen is None else seen
    node = manifest["nodes"].get(node_id, {})
    for parent in node.get("depends_on", {}).get("nodes", []):
        if parent not in seen:
            seen.add(parent)
            upstream(manifest, parent, seen)
    return seen

print(sorted(upstream(manifest, "model.shop.fct_sales")))
```

Sources are not in `nodes` in this sketch, so `.get(node_id, {})` lets the walk stop there. The `seen` set prevents visiting a shared ancestor twice (and an infinite loop if the graph had a cycle).

## Common mistakes

- `json.loads` on a file object: `TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper`. Use `json.load(f)`.
- `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`: empty string, an HTML error page, or a BOM. Print `text[:100]`.
- Chaining `["a"]["b"]` on data that sometimes has `null`.
- Using `json.load` on a JSONL file: `Extra data: line 2 column 1`.

## What to take away

1. JSON maps to dict/list/str/number/bool/None; `dumps`/`loads` for strings, `dump`/`load` for files.
2. `.get(k, {})` guards against missing keys, not `null` values; use `or {}`.
3. JSONL: one object per line, stream it, catch `JSONDecodeError`, count what you skip.
4. Graphs like dbt manifests are dicts of ids; walk them with a `seen` set.
