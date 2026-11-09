`transfer(conn, src, dst, amount)` moves `amount` between two rows of the `acct(id, balance)` table. The current version works for good input, but when the destination account does not exist it raises `ValueError` **after the money has already left the source account**. An overdraft is also committed before it is noticed.

Fix it so the transfer is all-or-nothing: on any `ValueError` (unknown account, or insufficient funds in `src`) both balances stay exactly as they were.

```python
transfer(conn, 1, 2, 30)     # ok
transfer(conn, 1, 99, 30)    # ValueError, balances unchanged
transfer(conn, 1, 2, 10_000) # ValueError (insufficient funds), unchanged
```
