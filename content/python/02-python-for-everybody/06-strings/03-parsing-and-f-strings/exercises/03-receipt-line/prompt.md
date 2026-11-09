Write `receipt_line(item, qty, price)`. Return one line of a receipt in this exact layout:

- the item name, left-aligned in a field 10 characters wide (padded with spaces on the right),
- a space, then `x`, then the quantity,
- a space, then the total cost (`qty * price`) with two decimals, right-aligned in a field 8 characters wide.

`receipt_line("tea", 3, 1.5)` returns `"tea        x3     4.50"`.
