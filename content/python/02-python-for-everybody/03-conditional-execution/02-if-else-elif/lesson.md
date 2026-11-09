+++
id = "everybody.conditional-execution.if-else-elif"
title = "Making decisions with if, else and elif"
minutes = 25
+++

# Making decisions with if, else and elif

Now we can ask questions, so let us make the program act on the answers. The tool is the `if` statement.

## The `if` statement

An **if statement** runs some code only when a condition is true:

```python
temperature = 4
if temperature < 10:
    print("Take a coat")
print("Have a nice day")
```

The condition `temperature < 10` is a boolean expression. Because it is `True`, the indented line runs. The last line is not indented, so it always runs. Both lines are shown here.

Look at the shape:

- the word `if`,
- a condition,
- a **colon** `:` at the end of the line,
- the **indented block** below it, the lines that belong to the `if`.

Python uses indentation (the spaces at the start of a line) to see which lines belong together. The usual choice is four spaces. Every line in a block must be indented by the same amount. If the condition is `False`, the whole block is skipped.

## Alternative execution: `else`

An `else` gives the program something to do when the condition is false. Exactly one of the two blocks will run.

```python
age = 15
if age >= 18:
    print("Adult ticket")
else:
    print("Child ticket")
```

This shows `Child ticket`. The `else` line has its own colon and lines up with the `if`.

## Chained conditionals: `elif`

What if there are more than two possibilities? Use `elif` (short for "else if"), as many times as you like:

```python
score = 72
if score >= 90:
    grade = "A"
elif score >= 70:
    grade = "B"
elif score >= 50:
    grade = "C"
else:
    grade = "F"
print(grade)
```

Python checks the conditions from top to bottom and runs the block of the **first** one that is true, then skips the rest. With a score of 72, the first test fails, the second passes, so the grade is `B`. We never even look at the third test.

That is why the order matters. If you tested `score >= 50` first, then everyone with 50 or more would get a `C`, even someone with 95. Put the narrowest condition first.

The final `else` is optional. It catches everything left over. Without it, it is possible that no block runs at all.

## Nested conditionals

One `if` can sit inside another. This is a **nested conditional**. The inner statement is indented one more step.

```python
is_member = True
age = 70
if is_member:
    if age >= 65:
        price = 4
    else:
        price = 6
else:
    price = 9
print(price)
```

Here members who are 65 or over pay 4, other members pay 6, and everyone else pays 9. The result is 4.

Nesting works, but deep nesting gets hard to read. Often you can flatten it with a logical operator:

```python
if is_member and age >= 65:
    price = 4
```

## Returning from inside an `if`

In a function, a `return` ends the function straight away. This lets you write decisions without `else`:

```python
def describe(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"
```

When `n` is negative, the first `return` ends the function and the rest never run. Many programmers like this style because it avoids extra levels of indentation.

## Common mistakes

- **Forgetting the colon** at the end of the `if`, `elif` or `else` line. That is a `SyntaxError`.
- **Forgetting to indent**, or indenting with different amounts. Python reports an `IndentationError`.
- **Using `=` instead of `==`** in the condition.
- **Putting a condition on `else`.** `else` never has a condition; use `elif` for that.
- **Writing the tests in the wrong order** in a chain, so an early broad test steals the cases.
- **Using several separate `if` statements** when you want exactly one answer. Separate `if`s are all checked; `elif` is skipped once something matched.

## What to take away

1. `if condition:` followed by an indented block runs the block only when the condition is true.
2. `else` is the "otherwise" block; `elif` adds more conditions in a chain.
3. Only the first matching block in a chain runs, so order the tests with care.
4. Indentation shows which lines belong to which block.
