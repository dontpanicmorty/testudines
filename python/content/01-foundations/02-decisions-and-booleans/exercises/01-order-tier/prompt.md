Translate this SQL into Python:

```sql
CASE WHEN amount >= 1000 THEN 'enterprise'
     WHEN amount >= 100  THEN 'standard'
     WHEN amount > 0     THEN 'small'
     ELSE 'none' END
```

Write `order_tier(amount)` returning the tier name.

```python
order_tier(2500)  # "enterprise"
order_tier(100)   # "standard"
order_tier(0.5)   # "small"
order_tier(0)     # "none"
order_tier(-3)    # "none"
```
