+++
id = "everybody.conditional-execution.short-circuit-and-tracebacks"
title = "Short-circuiting, guardians and tracebacks"
minutes = 25
+++

# Short-circuiting, guardians and tracebacks

This lesson is about two things: how Python can skip work in a logical expression, which lets you protect risky code, and how to read the error report Python gives you when something fails.

## Short-circuit evaluation

Remember `and` is true only if both sides are true. Now think about `False and anything`. As soon as Python sees the left side is `False`, it knows the whole answer must be `False`. Why bother with the right side? So it does not look at it. This is called **short-circuit evaluation**.

The same happens with `or`. If the left side is `True`, the answer is `True`, and the right side is skipped.

```python
x = 3
print(x > 5 and x / 0 > 1)
```

You might expect a crash from `x / 0`. But `x > 5` is `False`, so Python stops there and prints `False`. The dangerous part never runs.

Short-circuiting reads from left to right, so the order of the parts matters.

## The guardian pattern

You can use that behaviour on purpose. Put a safety check on the left, and the risky check on the right. The left side **guards** the right side. This is the **guardian pattern**.

Suppose we want to know whether a divide gives more than 2:

```python
a = 10
b = 0
print(b != 0 and a / b > 2)
```

Because `b != 0` is `False`, the division is never attempted, and the result is `False`. Swap the order and you get a `ZeroDivisionError`.

Another classic. A string may be empty, and asking for its first letter would fail:

```python
word = ""
print(len(word) > 0 and word[0] == "t")
```

Python says `False` without touching `word[0]`. With any word that starts with "t", the answer is `True`.

Compare this with the alternative, a `try` block. The guardian is neat when the check is a simple condition. Use `try` when the problem is hard to predict.

## Reading a traceback

When an exception is not caught, Python prints a **traceback**: a report of where things went wrong. It looks like this:

```
Traceback (most recent call last):
  File "shop.py", line 7, in <module>
    total = price_with_tax(item_cost)
  File "shop.py", line 3, in price_with_tax
    return cost * rate
NameError: name 'rate' is not defined
```

Read it from the **bottom up**:

1. **The last line** names the kind of error and gives a message: `NameError: name 'rate' is not defined`. Start here.
2. **The line above it** shows the code that failed, and `File "shop.py", line 3` tells you where.
3. **The lines further up** show how the program got there: line 7 called `price_with_tax`, which crashed at line 3.

For most errors, the last line and the line number are enough to find the cause. Do not be put off by the length. A traceback is a map, not a punishment.

## Debugging tips for conditions

Some typical problems when you work with decisions:

- **Print the condition.** If an `if` does not do what you expect, `print` the condition itself and look at whether it is `True` or `False`.
- **Check the boundaries.** Test values exactly on the edge of each range (for example 49, 50 and 51).
- **Write down the plan before the code.** List the cases in plain language and check every case is covered.
- **Read the message type.** `IndentationError` means the spacing is wrong; `SyntaxError` on an `if` line usually means a missing colon.
- **Beware of silent branches.** If no condition matches and there is no `else`, nothing happens at all. A missing result can be a clue.

## Getting the error name inside a program

Sometimes you want your program to report what went wrong instead of crashing. You can catch the exception and look at its type:

```python
try:
    value = int("abc")
except Exception as problem:
    print(type(problem).__name__)
```

This shows `ValueError`. `except Exception as problem` catches nearly any error and stores it in `problem`. We use `type(problem).__name__` to get its name as text.

## Common mistakes

- **Putting the risky check first.** `a / b > 2 and b != 0` still crashes; the guard must come first.
- **Reading the traceback from the top.** The answer is at the bottom.
- **Assuming the line number is exactly right.** Sometimes the real mistake is just above, especially for brackets.
- **Guarding against the wrong thing.** The guard must test exactly what could go wrong.
- **Forgetting that `or` short-circuits the other way.** It stops on the first `True`.

## What to take away

1. `and` stops at the first false part; `or` stops at the first true part.
2. Put the safe check on the left of `and` to guard the risky check on the right.
3. Read a traceback from the bottom: error type, then the line, then the call path.
4. Print conditions and test boundary values when debugging decisions.
