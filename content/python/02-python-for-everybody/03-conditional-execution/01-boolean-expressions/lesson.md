+++
id = "everybody.conditional-execution.boolean-expressions"
title = "True, False and comparisons"
minutes = 20
+++

# True, False and comparisons

Up to now, every line of your programs has run, one after the other. Real programs need to make choices: "if the password is wrong, show a message". To make choices, Python needs to ask yes-or-no questions. This lesson covers those questions.

## Boolean expressions

A **boolean expression** is a question whose answer is either `True` or `False`. These two words are the only values of the type `bool`. Notice the capital letters: `True` and `False` are Python words, but `true` is not.

You make a boolean expression with a **comparison operator**:

```python
print(5 == 5)
print(5 == 6)
print(5 != 6)
```

This shows `True`, `False` and `True`. The double equals `==` asks "is this equal to that?". Remember, a single `=` stores a value in a variable, while `==` compares two values. It is the most common beginner mix-up.

Here are all six comparison operators:

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | equal to | `3 == 3` | `True` |
| `!=` | not equal to | `3 != 4` | `True` |
| `<` | less than | `3 < 4` | `True` |
| `>` | greater than | `3 > 4` | `False` |
| `<=` | less than or equal to | `4 <= 4` | `True` |
| `>=` | greater than or equal to | `3 >= 4` | `False` |

There is no `=<` or `=>`. The equals sign always comes second.

Comparisons work on text, too. `"tea" == "tea"` is `True`, and capital letters count: `"Tea" == "tea"` is `False`. Using `<` on text puts words in dictionary-like order, with capitals sorting before lower-case letters.

You can store a boolean in a variable like any other value:

```python
age = 17
is_adult = age >= 18
print(is_adult)
```

This shows `False`. The expression `age >= 18` is worked out, and the answer is stored in `is_adult`.

## Logical operators

Sometimes one question is not enough. Three **logical operators** combine booleans: `and`, `or` and `not`.

- `a and b` is `True` only when **both** are true.
- `a or b` is `True` when **at least one** is true.
- `not a` flips the answer: `not True` is `False`.

```python
age = 25
has_ticket = True
print(age >= 18 and has_ticket)
print(age < 12 or age > 65)
print(not has_ticket)
```

This shows `True`, `False` and `False`. In the first line both parts are true. In the second line neither is.

It helps to see all the possible combinations:

| a | b | `a and b` | `a or b` |
|---|---|-----------|----------|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

When you mix them, `not` is worked out first, then `and`, then `or`. Brackets make your intention clear, so use them freely:

```python
print(True or False and False)      # True
print((True or False) and False)    # False
```

## A shortcut for ranges

In maths you write `1 <= x <= 10`. Python allows this too:

```python
x = 7
print(1 <= x <= 10)
```

This is `True`, and it reads naturally. It means the same as `1 <= x and x <= 10`.

## Any number can be a condition

Python also treats other values as true or false when asked. The number `0`, an empty string `""`, and the value `None` count as false. Almost everything else counts as true. You can see this with `bool()`:

```python
print(bool(0))         # False
print(bool(3))         # True
print(bool(""))        # False
print(bool("hello"))   # True
```

For now, prefer explicit comparisons like `count > 0`, which are clearer to read.

## Common mistakes

- **Writing `=` instead of `==`.** `x = 5` stores; `x == 5` asks.
- **Splitting a comparison wrongly.** `x == 1 or 2` does not mean "x is 1 or 2". Write `x == 1 or x == 2`.
- **Writing `true` or `false` in lower case.** Python only knows `True` and `False`.
- **Comparing text and numbers.** `"5" == 5` is `False`, because they are different types.
- **Mixing up `and` and `or`.** For a rule like "not a child and not a senior", say it out loud before you write it.

## What to take away

1. A boolean expression has the value `True` or `False`.
2. Comparison operators are `==`, `!=`, `<`, `>`, `<=` and `>=`.
3. `and`, `or` and `not` combine booleans.
4. Chained comparisons such as `1 <= x <= 10` are allowed.
