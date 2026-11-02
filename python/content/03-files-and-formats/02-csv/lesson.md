+++
id = "files-and-formats.csv"
title = "CSV with the csv module"
minutes = 25
+++

# CSV with the `csv` module

CSV is the cockroach of data formats: ugly, universal, indestructible. In the warehouse a `COPY INTO` with a file format does the parsing and typing. In Python the `csv` module splits rows for you, and typing is **your** job.

> **SQL bridge.** `FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ';' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')` maps to `csv.DictReader(f, delimiter=";")`. Header handling and quoting are built in.

## Why not `line.split(",")`?

> **Predict first.** What does splitting this line on commas give?

```python
line = 'INV-1,"Smith, Jane",42.50'
print(line.split(","))
```

The quoted comma breaks it into four fields. Quoting rules (embedded commas, quotes, even newlines) are exactly why you use a real parser.

## DictReader

`DictReader` uses the first row as keys and yields one dict per row.

```python
import csv
import io

data = 'id,name,amount\n1,"Smith, Jane",42.50\n2,Bo,7\n'
reader = csv.DictReader(io.StringIO(data))
print(reader.fieldnames)
for row in reader:
    print(row)
```

`io.StringIO` makes a string behave like a file, perfect for examples and tests. With a real file:

```python
# no-run
with path.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        ...
```

Always open CSV files with `newline=""`. The csv module then handles `\r\n` and newlines inside quoted fields correctly.

## Everything is a string

This is the single most important fact about CSV.

```python
import csv
import io

row = next(csv.DictReader(io.StringIO("id,amount,active\n7,19.5,true\n")))
print(row)
print(row["amount"] + row["amount"])      # concatenation, not addition
print(float(row["amount"]) * 2)
print(bool(row["active"] == "true"))
```

There is no inference. An empty cell is `""`, not `None`. The text `"false"` is truthy. Write one small function that turns a raw row dict into a typed record and call it at the edge:

```python
from decimal import Decimal

def to_record(row):
    return {
        "id": int(row["id"]),
        "amount": Decimal(row["amount"]) if row["amount"] else None,
        "active": row["active"].strip().lower() == "true",
    }

print(to_record({"id": "7", "amount": "", "active": "True"}))
```

## Delimiters and quoting

```python
import csv
import io

data = "id;note\n1;He said \"hi\"\n2;a|b\n"
for row in csv.DictReader(io.StringIO(data), delimiter=";"):
    print(row)
```

Other knobs: `quotechar`, `skipinitialspace=True` (for `a, b, c` style), and `csv.Sniffer` to guess a delimiter when you truly do not know. Prefer being told the format over guessing it.

If a row has more cells than the header, extras land under the key `None` (`restkey`). Fewer cells give `None` values (`restval`). Both are signs of a malformed row worth checking.

```python
import csv
import io

data = "a,b\n1,2,3\n4\n"
for row in csv.DictReader(io.StringIO(data)):
    print(row)
```

## DictWriter

```python
import csv
import io

rows = [{"id": 1, "name": "Smith, Jane"}, {"id": 2, "name": 'Say "hi"'}]
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=["id", "name"], lineterminator="\n")
w.writeheader()
w.writerows(rows)
print(buf.getvalue())
```

The writer quotes only where needed. `fieldnames` fixes column **order**, and a dict with an unexpected key raises `ValueError: dict contains fields not in fieldnames`. That is a feature: schema drift gets caught at write time. Use `extrasaction="ignore"` only when you mean to drop columns.

## Streaming

`DictReader` is lazy: it reads one row at a time. A generator keeps the pipeline lazy end to end.

```python
import csv
import io

def read_rows(f):
    for row in csv.DictReader(f):
        yield row

def big_orders(rows, minimum):
    for row in rows:
        if float(row["amount"]) >= minimum:
            yield row

src = io.StringIO("id,amount\n1,5\n2,50\n3,500\n")
print([r["id"] for r in big_orders(read_rows(src), 40)])
```

Nothing is held in memory beyond the current row. Only call `list(...)` when you really need all rows.

## Common mistakes

- Summing `row["amount"]` and getting `TypeError: unsupported operand type(s) for +: 'int' and 'str'`. Convert first.
- Opening without `newline=""` and ending up with blank lines in output on Windows.
- Header with trailing spaces (`"Customer Name "`) so `row["Customer Name"]` raises `KeyError`. Normalise headers when the source is not under your control.
- Reading a `DictReader` twice. It is exhausted after one pass.

## What to take away

1. Use `csv`, never `split(",")`.
2. Every value is a `str`; convert in one dedicated function.
3. Open with `newline=""` and an explicit encoding.
4. `DictWriter` fixes column order and rejects unknown keys.
5. Readers are lazy; keep pipelines streaming with generators.
