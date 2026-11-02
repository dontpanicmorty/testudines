# Collections cheat sheet

| Type | Literal | Ordered | Mutable | Duplicates | SQL analogue |
|---|---|---|---|---|---|
| `list` | `[1, 2]` | yes | yes | yes | ARRAY / one column |
| `tuple` | `(1, 2)` | yes | no | yes | one row, fixed |
| `dict` | `{"a": 1}` | insertion order | yes | unique keys | row / OBJECT / key-value |
| `set` | `{1, 2}` | no | yes | unique | `SELECT DISTINCT` |

## Lists

| Task | Python |
|---|---|
| Add one / many | `xs.append(x)`, `xs.extend(ys)` |
| Insert / remove | `xs.insert(i, x)`, `xs.remove(x)`, `xs.pop()` |
| Slice (copy) | `xs[1:3]`, `xs[-2:]`, `xs[::-1]` |
| Sorted copy / in place | `sorted(xs, key=f, reverse=True)`, `xs.sort()` |
| Copy | `xs.copy()`, `list(xs)`, `xs[:]` |
| Count / membership | `xs.count(x)`, `x in xs` |

```python
xs = [3, 1, 2]
print(sorted(xs), xs[::-1], xs[:2])
first, *rest = xs
print(first, rest)
```

## Dicts

| Task | Python | SQL analogue |
|---|---|---|
| Required / optional key | `d[k]`, `d.get(k, default)` | column / `COALESCE` |
| Keys, values, pairs | `d.keys()`, `d.values()`, `d.items()` | |
| Merge (new dict) | `{**a, **b}`, `a \| b` | |
| Set default | `d.setdefault(k, [])` | |
| Remove | `d.pop(k, None)`, `del d[k]` | |
| Invert / lookup table | `{r["id"]: r for r in rows}` | index on id |

```python
d = {"id": 1, "plan": "pro"}
print(d.get("region", "n/a"), {**d, "plan": "team"})
print({k: v for k, v in d.items() if k != "id"})
```

## Sets

| Operation | Python | SQL |
|---|---|---|
| Distinct | `set(xs)` | `DISTINCT` |
| Union / intersect / except | `a \| b`, `a & b`, `a - b` | `UNION`, `INTERSECT`, `EXCEPT` |
| Symmetric difference | `a ^ b` | |
| Subset test | `a <= b` | |
| Add / discard | `s.add(x)`, `s.discard(x)` | |

```python
a, b = {1, 2, 3}, {2, 3, 4}
print(sorted(a | b), sorted(a & b), sorted(a - b))
```

## collections and itertools

| Tool | Use | SQL analogue |
|---|---|---|
| `Counter(xs)` | counts; `.most_common(n)` | `COUNT(*) GROUP BY` |
| `defaultdict(list)` | group into lists | `ARRAY_AGG GROUP BY` |
| `defaultdict(float)` | sum per key | `SUM GROUP BY` |
| `sorted(rows, key=lambda r: (r["a"], -r["b"]))` | multi-column order | `ORDER BY a, b DESC` |
| `zip(a, b)`, `enumerate(xs, 1)` | pair / number items | positional join / `ROW_NUMBER` |
| `itertools.islice`, `chain`, `groupby` | lazy slice / concat / adjacent groups | `LIMIT`, `UNION ALL` |

```python
from collections import Counter, defaultdict
print(Counter("abca").most_common(1))
g = defaultdict(list)
for k, v in [("a", 1), ("b", 2), ("a", 3)]:
    g[k].append(v)
print(dict(g))
```

## Comprehensions

```python
nums = [1, -2, 3]
print([n * 2 for n in nums if n > 0])        # SELECT n*2 WHERE n > 0
print({n: n * n for n in nums})              # dict
print({n % 2 for n in nums})                 # set
print(sum(n for n in nums if n > 0))         # generator expression
```

## Gotchas

- `{}` is an empty dict; use `set()` for an empty set.
- `b = a` aliases a list or dict; copy with `.copy()` (shallow) when you need independence.
- Mutating methods (`append`, `sort`, `update`) return `None`.
- Keys and set members must be hashable: tuples yes, lists no.
