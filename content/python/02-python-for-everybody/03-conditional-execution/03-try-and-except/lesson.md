+++
id = "everybody.conditional-execution.try-and-except"
title = "Catching errors with try and except"
minutes = 25
+++

# Catching errors with try and except

Programs often receive input they cannot control. Someone types "abc" where you wanted a number, or a calculation divides by zero. Normally Python stops with an error, which is no fun for the user. With `try` and `except` you decide what happens instead.

## An error that stops everything

Suppose we ask for a number and convert it:

```python
text = "forty"
number = int(text)
print("Got", number)
```

Python stops on the second line with a `ValueError`, and the `print` never runs. This kind of error is called an **exception**. By default an exception ends the program, with a message.

## Catching the exception

Put the risky code in a `try` block, and the plan B in an `except` block:

```python
text = "forty"
try:
    number = int(text)
    print("Got", number)
except:
    print("That was not a whole number")
```

This shows `That was not a whole number`. Here is how it works:

1. Python starts running the `try` block.
2. If every line works, the `except` block is skipped.
3. If a line fails, Python jumps straight to the `except` block. The rest of the `try` block is skipped.
4. After that, the program continues normally with whatever follows.

Notice that `Got` was never printed. The error happened on the line before it.

## Naming the exception

A bare `except:` catches every error, including ones you did not think of, such as a typo in a variable name. It is better to name the kind of error you expect:

```python
try:
    number = int(text)
except ValueError:
    number = 0
```

If a different kind of error occurs inside the `try`, it is not caught, and the program stops as normal. That is good: you hear about the surprise.

Here are the exceptions you will see most often:

- `ValueError`: the type is right but the value is not, such as `int("abc")`.
- `TypeError`: wrong kind of value, such as `"a" + 1`.
- `ZeroDivisionError`: dividing by zero.
- `NameError`: using a name that does not exist.
- `IndexError`: asking for a position that is not there, such as `"abc"[10]`.

You can list several in one `except`, or write several `except` blocks:

```python
try:
    result = 100 / int(text)
except ValueError:
    result = None            # text was not a number
except ZeroDivisionError:
    result = None            # text was 0
```

## Using the result

A common pattern is a function that tries a conversion and returns a fallback value if it fails:

```python
def number_or_zero(text):
    try:
        return int(text)
    except ValueError:
        return 0
```

Calling `number_or_zero("17")` gives `17`; `number_or_zero("hello")` gives `0`.

Keep the `try` block small. Put only the risky line or lines inside, so you do not accidentally hide errors in code that has nothing to do with the problem.

## Asking again

You will see in chapter 5 how to repeat. Once you can, the usual pattern is to keep asking until the answer is good: try the conversion, and if it fails, tell the user and ask again.

## Common mistakes

- **Catching too much.** A bare `except:` hides typos and real bugs. Name the error.
- **A huge `try` block.** Wrap only the line that can fail.
- **Forgetting the colon** after `try` or `except`, or forgetting to indent.
- **Expecting code after the failing line to run.** It is skipped when an exception happens.
- **Using `try` for something an `if` can check clearly.** Both are fine; pick whichever makes the intent obvious.
- **Silently doing nothing.** If you swallow an error, tell the user or return a clear fallback.

## What to take away

1. An error at run time is an exception; it stops the program unless you catch it.
2. `try` holds the risky code; `except` holds the plan B.
3. Name the exception you expect, such as `ValueError`.
4. Keep the `try` block small.
