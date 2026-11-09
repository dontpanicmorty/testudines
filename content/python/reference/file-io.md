# File I/O cheat sheet

## Paths

```python
from pathlib import Path
p = Path("data") / "raw" / "orders.csv"
p.name; p.stem; p.suffix; p.parent; p.with_suffix(".json")
p.exists(); p.is_file(); p.mkdir(parents=True, exist_ok=True)
sorted(p.parent.glob("*.csv")); sorted(p.parent.rglob("*.csv"))
```

## Text and modes

| Mode | Meaning |
|---|---|
| `"r"` | read (default) |
| `"w"` | write, **truncates** |
| `"a"` | append |
| `"x"` | create, fail if exists |
| `"b"` | add for bytes |

```python
text = p.read_text(encoding="utf-8")
p.write_text(text, encoding="utf-8")
with p.open(encoding="utf-8") as f:
    for line in f:                 # streams; line keeps "\n"
        line = line.rstrip("\n")
```

Excel exports: `encoding="utf-8-sig"` strips the BOM.

## Formats

| Format | Read | Write | Watch out |
|---|---|---|---|
| CSV | `csv.DictReader(f)` | `csv.DictWriter(f, fieldnames)` | open with `newline=""`; every value is `str` |
| JSON | `json.load(f)` / `json.loads(s)` | `json.dump(obj, f)` / `json.dumps(obj)` | no dates or `Decimal`; `null` is `None` |
| JSONL | `json.loads(line)` per line | `f.write(json.dumps(o) + "\n")` | catch `json.JSONDecodeError`, count skips |
| YAML | `yaml.safe_load(f)` | `yaml.safe_dump(obj)` | never `yaml.load`; quote `"no"`, `"007"` |

## Config and secrets

- Layers, lowest to highest: code defaults, file, environment, flags.
- `os.environ.get("NAME")` returns `str` or `None`; convert types yourself.
- Secrets live in the environment, never in code or committed files; never log them.

## Tests

`tmp_path` (pytest) is a fresh `Path` per test; make functions take paths as arguments.
