`process(t)` turns exported invoice CSV text into a report. It works, but it is one 28-line function with one-letter names, so nobody dares touch it.

Refactor it into small, well-named functions **without changing what `process` returns**. The check requires:

- `process` still exists and returns the same text;
- at least three functions in the file;
- no function longer than 15 lines.

Behaviour: rows whose `status` (case-insensitive, trimmed) is `paid` count; amounts may have a `$`; totals per customer are listed highest first (ties by name) as `name: 12.50`, followed by a `TOTAL: ...` line.

```python
process("customer,amount,status\nAda,$10.5,paid\nGrace,3,open\nAda,2,PAID")
# 'Ada: 12.50\nTOTAL: 12.50'
```
