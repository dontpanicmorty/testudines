# Strings cheat sheet

| Task | Python | SQL analogue |
|---|---|---|
| Trim | `s.strip()` / `lstrip()` / `rstrip()` | `TRIM` |
| Upper / lower / title | `s.upper()`, `s.lower()`, `s.title()` | `UPPER`, `LOWER`, `INITCAP` |
| Length | `len(s)` | `LENGTH` |
| Substring | `s[2:5]` (0-based, stop excluded) | `SUBSTR(s, 3, 3)` |
| Contains | `"ab" in s` | `LIKE '%ab%'` |
| Starts / ends with | `s.startswith("ab")`, `s.endswith(".csv")` | `LIKE 'ab%'` |
| Find position | `s.find("x")` (-1 if absent) | `POSITION`, `CHARINDEX` |
| Replace | `s.replace("a", "b")` | `REPLACE` |
| Split to list | `s.split(",")`, `s.split()` | `SPLIT` |
| Join list | `",".join(parts)` | `LISTAGG`, `ARRAY_TO_STRING` |
| Pad | `s.zfill(5)`, `s.ljust(8)`, `s.rjust(8)` | `LPAD`, `RPAD` |
| Concatenate | `a + b`, `f"{a}{b}"` | `a \|\| b` |
| Is digits? | `s.isdigit()` | `TRY_CAST(s AS INT) IS NOT NULL` |
| To number | `int(s)`, `float(s)` | `CAST` |

```python
s = "  Ada,Lovelace ,pro "
parts = [p.strip() for p in s.split(",")]   # ['Ada', 'Lovelace', 'pro']
print(parts)
print("-".join(parts).lower())
print(f"{3.14159:.2f} | {1234567:,} | {'x':>5} | {7:03d}")
print("report.csv".removesuffix(".csv"))
print("a b  c".split(), "a b  c".split(" "))
```

## f-string format specs

| Spec | Meaning | Example |
|---|---|---|
| `:.2f` | 2 decimals | `f"{x:.2f}"` |
| `:,` | thousands separator | `f"{n:,}"` |
| `:>10` / `:<10` / `:^10` | align right / left / center | `f"{s:>10}"` |
| `:05d` | zero-pad integer | `f"{7:05d}"` |
| `:.1%` | percentage | `f"{0.256:.1%}"` |
| `!r` | `repr()` of the value | `f"{s!r}"` |

## Gotchas

- Strings are immutable: `s.strip()` returns a new string, so assign it.
- `split(",")` on `""` gives `[""]`, not `[]`.
- `s.split()` (no argument) collapses runs of whitespace; `s.split(" ")` does not.
- `"5" + 5` raises `TypeError`; convert with `int()` or an f-string.
- Compare text after normalising: `a.strip().lower() == b.strip().lower()`.
