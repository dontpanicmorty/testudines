+++
id = "everybody.functions.return-values"
title = "Fruitful and void functions"
minutes = 25
+++

# Fruitful and void functions

Some functions give you an answer to use. Others just do something, like displaying a message. This lesson explains the difference and how to build both.

## Fruitful functions

A **fruitful function** produces a value for the caller. Functions like `max` and `len` are fruitful: you call them and get something back. You write your own with `return`:

```python
def double(number):
    return number * 2

answer = double(21)
print(answer)
```

When Python reaches `return`, it works out the expression, ends the function immediately and hands the value back to the place where the function was called. Here, `double(21)` becomes `42`, which is stored in `answer`.

You can use a call anywhere you could use a value:

```python
print(double(3) + double(4))
```

This shows `14`.

## Void functions

A **void function** does something useful, such as printing, but does not give back a value:

```python
def show_total(price, quantity):
    print("Total:", price * quantity)
```

If you call it, you see the message, but there is nothing to store. What happens if you try?

```python
result = show_total(2, 3)
print(result)
```

This displays `Total: 6` and then `None`. Python gives a function with no `return` the special value `None`, which means "nothing here".

This is a common beginner mix-up. A function that **prints** an answer is not the same as one that **returns** it. Only a returned value can be stored, compared or used in more calculations.

```python
def add_printing(a, b):
    print(a + b)

def add_returning(a, b):
    return a + b

total = add_returning(2, 3) + 10    # 15, works
oops = add_printing(2, 3) + 10      # prints 5, then crashes: TypeError
```

The second line fails because `add_printing(2, 3)` is `None`, and `None + 10` makes no sense.

Rule of thumb: let functions *return* results, and let a small part of the program at the outer level do the printing.

## Returning from the middle

A function stops at the first `return` it reaches. This makes it easy to handle special cases first:

```python
def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value
```

`clamp(15, 0, 10)` hits the second `if` and returns `10`. `clamp(5, 0, 10)` skips both and returns `5`.

Every path through a fruitful function should end in a `return`. If one path forgets, the caller silently gets `None`.

```python
def sign(n):
    if n > 0:
        return "plus"
    elif n < 0:
        return "minus"
    # n == 0: no return here, so the answer is None!
```

Calling `sign(0)` gives `None`. Add a final `return "zero"` to cover it.

## Returning booleans

A function that answers a yes-or-no question usually returns `True` or `False`. The condition itself is already a boolean, so you can return it directly:

```python
def is_teen(age):
    return 13 <= age <= 19
```

There is no need to write `if ...: return True else: return False`.

## A fruitful function is easy to test

When a function returns a value, you can check it with a single line:

```python
print(is_teen(15))   # True
print(is_teen(30))   # False
```

That is exactly how the exercises in this course are marked: they call your function and compare what it returns. Functions that only print are harder to test, which is another reason to prefer `return`.

## Common mistakes

- **Printing instead of returning.** The caller receives `None`.
- **Forgetting `return` in one branch** of an `if` chain.
- **Writing code after a `return`.** It is never reached.
- **Forgetting to use the result.** Writing `double(5)` alone on a line calculates and throws the answer away. Store it or print it.
- **Returning a value of the wrong type.** If a test expects a number and your function returns text like `"5"`, they are not equal.

## What to take away

1. A fruitful function returns a value with `return`; the call is replaced by that value.
2. A void function has no `return`, so it gives back `None`.
3. Returning is not the same as printing; only a returned value can be reused.
4. A function ends at its first `return`; make sure every path returns something.
