+++
id = "wrangling-in-pure-python.dates-times-and-decimals"
title = "Dates, times and decimals"
minutes = 30
+++

# Dates, times and decimals

Two things go wrong silently in analytics: time zones and money. A report that is off by one day at midnight UTC, or by a cent per line across ten million lines, passes every eyeball test and fails the audit. Python gives you precise tools for both; the skill is knowing which type to hold.

> **SQL bridge.** `DATE`, `TIMESTAMP_NTZ`, `TIMESTAMP_TZ` and `NUMBER(18,2)` map to `datetime.date`, naive `datetime`, aware `datetime` and `Decimal`. `DATEADD`, `DATEDIFF` map to `timedelta` arithmetic.

## date, datetime, timedelta

```python
from datetime import date, datetime, timedelta

d = date(2025, 6, 30)
print(d, d.year, d.month, d.weekday())        # Monday is 0
print(d + timedelta(days=1))                   # DATEADD(day, 1, d)
print(date(2025, 7, 15) - d)                   # a timedelta
print((date(2025, 7, 15) - d).days)            # DATEDIFF(day, d, ...)

dt = datetime(2025, 6, 30, 23, 30)
print(dt + timedelta(hours=1))
print(dt.date(), dt.time())
print(dt.isoformat())
```

A `timedelta` holds days, seconds and microseconds. There is no "months" unit, because a month has no fixed length. For month arithmetic compute from `year` and `month`:

```python
from datetime import date

def first_of_next_month(d):
    return date(d.year + (d.month == 12), d.month % 12 + 1, 1)

print(first_of_next_month(date(2025, 12, 17)), first_of_next_month(date(2025, 6, 30)))
```

## Parsing and formatting

```python
from datetime import datetime

dt = datetime.strptime("20 Jun 2025 14:05", "%d %b %Y %H:%M")
print(dt)
print(dt.strftime("%Y-%m-%d"), dt.strftime("%A %d %B"))
print(datetime.fromisoformat("2025-06-05T00:48:57"))
```

`strptime` parses with a format, `strftime` formats. `fromisoformat` handles ISO 8601 strings, the format you should be exchanging whenever you control both ends.

## Naive vs aware

A **naive** datetime has no time zone: it is just numbers on a clock, and means whatever the author had in mind. An **aware** one carries an offset. Mixing them is an error, and that is a good thing.

> **Predict first.** What happens here?

```python
from datetime import datetime, timezone

naive = datetime(2025, 6, 5, 12, 0)
aware = datetime(2025, 6, 5, 12, 0, tzinfo=timezone.utc)
print(naive == aware)
try:
    print(aware - naive)
except TypeError as e:
    print("TypeError:", e)
```

Equality is `False` (they are not comparable instants), and subtraction raises `TypeError: can't subtract offset-naive and offset-aware datetimes`.

Rules that prevent most bugs:

1. **Store and compute in UTC** (aware datetimes), convert to local time only to display.
2. Attach the zone explicitly when you know it: `naive.replace(tzinfo=timezone.utc)`.
3. Convert between zones with `.astimezone(...)`.
4. Never call `datetime.now()` or `utcnow()` deep inside logic. Use `datetime.now(timezone.utc)` at the edge and **pass the value in**, so tests are deterministic.

```python
from datetime import datetime, timedelta, timezone

event = datetime.fromisoformat("2025-06-05T23:30:00+02:00")   # aware, +02:00
utc = event.astimezone(timezone.utc)
print(event, "->", utc)

cet = timezone(timedelta(hours=2))
print(utc.astimezone(cet).date(), utc.date())    # the calendar date differs!
```

The same instant is June 5 in one zone and June 5 or 6 in another depending on the hour. Grouping "events per day" must say **which** zone defines a day.

(For named zones with daylight saving, the standard library's `zoneinfo.ZoneInfo("Europe/Berlin")` does the work; a fixed `timezone(timedelta(...))` does not know about DST.)

## Decimal for money

> **Predict first.** What does each line print?

```python
print(0.1 + 0.2)
print(sum([0.1] * 10) == 1.0)
print(round(2.675, 2))
```

Floats are binary fractions: `0.1` cannot be represented exactly. `Decimal` stores base-10 digits.

```python
from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2"))
print(sum([Decimal("0.1")] * 10) == Decimal("1.0"))
print(Decimal(0.1))               # converting a float imports its error
print(Decimal("0.1"))             # always build from a string
```

Always construct from a **string** (or int), never from a float.

### Rounding is a business rule

`Decimal` rounding is explicit. Pick the mode your finance team uses.

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

x = Decimal("2.675")
cents = Decimal("0.01")
print(x.quantize(cents, rounding=ROUND_HALF_UP))     # 2.68, what people expect
print(x.quantize(cents, rounding=ROUND_HALF_EVEN))   # 2.68
print(Decimal("2.665").quantize(cents, rounding=ROUND_HALF_EVEN))  # 2.66, banker's rounding
print(Decimal("2.665").quantize(cents, rounding=ROUND_HALF_UP))    # 2.67
```

Python's built-in `round()` on floats uses banker's rounding **and** float error, which is why `round(2.675, 2)` is `2.67`. Quantise **once at the end** of a calculation, not after every step, unless the business rule says each line is rounded.

When writing to a database or CSV, convert `Decimal` to `str` (`"19.99"`); for JSON, also use strings, since JSON numbers become floats in most readers.

## Common mistakes

- `TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'`. Decimals refuse to mix with floats, on purpose.
- `Decimal(19.99)` giving `19.989999999999998436805981327779591083526611328125`.
- `TypeError: can't compare offset-naive and offset-aware datetimes` when sorting mixed timestamps.
- `datetime.utcnow()` returns a *naive* datetime, which is why it is deprecated; use `datetime.now(timezone.utc)`.
- Counting days with `(b - a).days` on datetimes and forgetting partial days are truncated.

## What to take away

1. `date` for calendar days, aware `datetime` in UTC for instants, `timedelta` for differences.
2. Do not mix naive and aware; attach the zone at the edge and store UTC.
3. Pass "now" in as an argument.
4. Use `Decimal` built from strings for money; choose the rounding mode explicitly and quantise at the end.
