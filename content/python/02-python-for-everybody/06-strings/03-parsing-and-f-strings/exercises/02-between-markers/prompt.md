Write `between(text, opener, closer)`. Return the text that sits between the first `opener` and the first `closer` that comes after it. The markers are strings of any length. If either marker cannot be found, return an empty string.

`between("price: <12.50> only", "<", ">")` returns `"12.50"`. `between("[[x]]", "[[", "]]")` returns `"x"`.
