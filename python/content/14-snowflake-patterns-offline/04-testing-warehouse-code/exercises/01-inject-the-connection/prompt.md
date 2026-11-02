`daily_total(day)` opens a real Snowflake connection internally, so it cannot be tested offline (calling it raises `RuntimeError`). Refactor it into `daily_total(connect, day)` where `connect` is a zero-argument factory returning a connection.

Behaviour:

- run `SELECT SUM(amount) FROM orders WHERE order_date = %(day)s` with params `{"day": day}` on a cursor that is closed afterwards;
- return the sum as a `float`, or `0.0` when the sum is `NULL` (no rows) ;
- close the connection **always**, including when the query raises (the exception still propagates).

```python
daily_total(lambda: fake_conn, "2026-11-02")    # 125.5
```
