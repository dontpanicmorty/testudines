# Dates, times and decimals cheat sheet

## Types

| Type | Use | SQL analogue |
|---|---|---|
| `date` | calendar day | `DATE` |
| `datetime` (naive) | clock reading, no zone | `TIMESTAMP_NTZ` |
| `datetime` (aware) | an instant | `TIMESTAMP_TZ` |
| `timedelta` | a duration | `DATEDIFF` result |
| `Decimal` | exact money | `NUMBER(18,2)` |

## Common calls

```python
from datetime import date, datetime, timedelta, timezone

date(2025, 6, 30) + timedelta(days=1)          # DATEADD
(date(2025, 7, 15) - date(2025, 6, 30)).days   # DATEDIFF(day)
datetime.strptime("20 Jun 2025", "%d %b %Y")   # parse
dt.strftime("%Y-%m-%d")                         # format
datetime.fromisoformat("2025-06-05T00:48:57")  # ISO 8601
dt.replace(tzinfo=timezone.utc)                 # attach a zone you KNOW
dt.astimezone(timezone.utc)                     # convert an aware value
datetime.now(timezone.utc)                      # now, aware (pass it in)
```

## Format codes

`%Y` year, `%m` month, `%d` day, `%H` hour (24h), `%M` minute, `%S` second, `%b` Jan, `%B` January, `%a` Mon, `%A` Monday, `%z` +0200.

## Rules

1. Store and compute in UTC (aware); convert only to display.
2. Never mix naive and aware: `TypeError: can't subtract offset-naive and offset-aware datetimes`.
3. Pass `now` into functions; do not call `now()` deep inside.
4. No `timedelta(months=...)`; use year/month arithmetic.
5. "Per day" grouping must say which zone defines the day.

## Decimal

```python
from decimal import Decimal, ROUND_HALF_UP
Decimal("0.1") + Decimal("0.2")                 # Decimal('0.3'), build from str
Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)   # 2.68
```

Decimals refuse to mix with floats. Quantise once at the end. Store as text or integer cents in files and databases.
