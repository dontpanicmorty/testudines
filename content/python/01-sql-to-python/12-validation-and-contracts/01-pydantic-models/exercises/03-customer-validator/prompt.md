`Customer` should normalise emails (strip, lowercase) and reject values without an `@`. Right now valid customers come out with `email=None`, and invalid ones are not rejected consistently. Fix the model so these hold:

```python
Customer(customer_id="7", email="  Ada@Example.COM ", signup_date="2024-06-12")
# customer_id=7, email='ada@example.com', signup_date=datetime.date(2024, 6, 12)
Customer(customer_id=1, email="nope", signup_date="2024-06-12")   # ValidationError
```
