+++
id = "wrangling-in-pure-python.cleaning-messy-exports"
title = "Cleaning messy exports"
minutes = 35
+++

# Cleaning messy exports

Every analyst has met the invoice export that someone "tidied" in a spreadsheet: padded names, dollar signs, three date formats, `N/A` in a numeric column, duplicates from a double upload. In SQL you would fix this in a staging model with `TRIM`, `LOWER`, `TRY_TO_DECIMAL`, `COALESCE` and `QUALIFY ROW_NUMBER() = 1`. Here is the same staging layer in plain Python.

> **SQL bridge.** `TRIM/LOWER` → `str.strip().lower()`. `TRY_TO_DECIMAL` → `Decimal` inside `try/except`. `COALESCE(x, 'unknown')` → `x or "unknown"`. `QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY ...) = 1` → a `seen` set.

The bundled file `messy_invoices.csv` has exactly these problems. Look at its header and the first few raw rows.

```python
import csv
import os
from pathlib import Path

path = Path(os.environ["DOJO_DATA"]) / "messy_invoices.csv"
with path.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    for row in list(reader)[:4]:
        print(row)
```

The header has a stray space (`'Customer Name '`) and inconsistent case (`AMOUNT`). Status values come as `Paid`, `PAID `, `paid`, or blank.

## Step 1: normalise headers

Fix the keys once, so downstream code uses predictable names.

```python
import re

def norm_header(h):
    h = h.strip().lower()
    h = re.sub(r"[^a-z0-9]+", "_", h)   # runs of anything else -> one underscore
    return h.strip("_")

print([norm_header(h) for h in ["Invoice #", "Customer Name ", "AMOUNT", "Invoice Date"]])
```

## Step 2: strip, case and missing values

Treat blanks and placeholders as one thing: **missing**, which in Python is `None`.

```python
MISSING = {"", "n/a", "na", "null", "none", "-"}

def clean_text(value):
    if value is None:
        return None
    value = value.strip()
    return None if value.lower() in MISSING else value

print(clean_text("  PAID "), clean_text("N/A"), clean_text("   "))
print("  margaret liskov ".strip().title())
```

`.title()` gives `Margaret Liskov`. (It is fine for these names; real names like `McDonald` or `de la Cruz` need more care, so only normalise case where the business wants it.)

## Step 3: amounts as `Decimal`

> **Predict first.** What will `float("$1,234.50")` do?

```python
# no-run
print(float("$1,234.50"))
```

```
ValueError: could not convert string to float: '$1,234.50'
```

Strip the currency symbol and thousands separators first, and use `Decimal` so cents stay exact (details in the next lesson).

```python
from decimal import Decimal, InvalidOperation

def parse_amount(text):
    text = (text or "").strip()
    if text.lower() in {"", "n/a", "na"}:
        return None
    try:
        return Decimal(text.replace("$", "").replace(",", ""))
    except InvalidOperation:
        raise ValueError(f"bad amount: {text!r}") from None

for t in ["$3,291.26", "1310.11", "N/A", ""]:
    print(repr(t), "->", parse_amount(t))
```

An unparseable amount raises, rather than quietly becoming zero. A *missing* amount is `None`: those are different facts.

## Step 4: several date formats

`datetime.strptime(text, fmt)` parses one format and raises `ValueError` otherwise. Try a list of known formats in order.

```python
from datetime import datetime

FORMATS = ["%Y-%m-%d", "%d %b %Y", "%m/%d/%Y"]

def parse_date(text):
    text = text.strip()
    for fmt in FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unrecognised date: {text!r}")

for t in ["2025-09-26", "20 Jun 2025", "05/26/2025"]:
    print(t, "->", parse_date(t))
```

Be careful with ambiguity: `07/07/2025` is fine, but `05/06/2025` could be May 6 or June 5. Here the data is US-style month first; confirm that with the source rather than guessing, and never include both `%d/%m/%Y` and `%m/%d/%Y` in one list.

## Step 5: dedupe

Duplicates in the file are exact repeats of the same invoice id. Keep the first occurrence, preserving order.

```python
rows = [{"id": "A"}, {"id": "B"}, {"id": "A"}, {"id": "C"}, {"id": "B"}]
seen = set()
unique = []
for r in rows:
    if r["id"] in seen:
        continue
    seen.add(r["id"])
    unique.append(r)
print([r["id"] for r in unique])
```

If the "latest wins" instead, load into a dict keyed by id: later rows overwrite earlier ones (`by_id[r["id"]] = r`).

## Putting it together

One function per concern, composed into a pipeline that never mutates its input:

```python
import csv
import os
import re
from collections import Counter
from decimal import Decimal
from pathlib import Path

def norm_header(h):
    return re.sub(r"[^a-z0-9]+", "_", h.strip().lower()).strip("_")

def clean_row(raw):
    row = {norm_header(k): v for k, v in raw.items()}
    amount = (row["amount"] or "").strip().replace("$", "").replace(",", "")
    return {
        "invoice": row["invoice"].strip(),
        "customer": row["customer_name"].strip().title(),
        "amount": Decimal(amount) if amount and amount.upper() != "N/A" else None,
        "status": (row["status"] or "").strip().lower() or None,
    }

path = Path(os.environ["DOJO_DATA"]) / "messy_invoices.csv"
with path.open(newline="", encoding="utf-8") as f:
    cleaned = [clean_row(r) for r in csv.DictReader(f)]

print(len(cleaned), "rows;", len({r["invoice"] for r in cleaned}), "unique invoices")
print(Counter(r["status"] for r in cleaned).most_common())
print(sum(1 for r in cleaned if r["amount"] is None), "rows with no amount")
```

Counting before and after (`120` rows, fewer unique) is a habit worth keeping: it is your equivalent of a row-count test.

## Common mistakes

- Cleaning in place and losing the raw value. Keep the raw file untouched and write clean output elsewhere.
- Turning `N/A` into `0` so totals look fine and quietly lie.
- `ValueError: time data '20 Jun 2025' does not match format '%Y-%m-%d'`: you have more formats than your list.
- Forgetting that `strip()` returns a new string.
- Dedupe by whole row when the real key is the invoice id.

## What to take away

1. Normalise headers first; then strip, case-fold and map placeholders to `None`.
2. Parse numbers with `Decimal`, dates with an explicit list of formats, and raise on the unparseable.
3. Missing is `None`, not zero.
4. Dedupe with a `seen` set (first wins) or a dict (last wins), by the business key.
5. Compare row counts before and after.
