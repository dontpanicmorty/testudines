Define a `LendingDesk` that tracks which member currently has which book title.

- `lend(title, member)` records the loan and returns `True`. If that title is already on loan, change nothing and return `False`.
- `give_back(title)` ends the loan and returns `True`, or returns `False` if the title was not on loan.
- `titles_for(member)` returns that member's titles as a sorted list (empty if none).
- `on_loan_count()` returns how many titles are currently out.

Two separate `LendingDesk()` instances must not share any data.
