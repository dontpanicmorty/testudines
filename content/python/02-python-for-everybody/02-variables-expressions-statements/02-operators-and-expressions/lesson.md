+++
id = "everybody.variables-expressions-statements.operators-and-expressions"
title = "Operators, expressions and order of operations"
minutes = 25
+++

# Operators, expressions and order of operations

Computers are excellent at arithmetic. In this lesson you will learn how to ask Python to calculate things, and in which order it works.

## Operators and operands

An **operator** is a symbol that tells Python to perform a calculation. The values it works on are called **operands**. In `4 + 3`, the `+` is the operator, and `4` and `3` are the operands.

Here are Python's arithmetic operators:

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | add | `7 + 2` | `9` |
| `-` | subtract | `7 - 2` | `5` |
| `*` | multiply | `7 * 2` | `14` |
| `/` | divide | `7 / 2` | `3.5` |
| `//` | floor divide | `7 // 2` | `3` |
| `%` | modulus | `7 % 2` | `1` |
| `**` | power | `7 ** 2` | `49` |

Two points surprise beginners. First, `/` always gives a `float`, even when the answer is whole: `8 / 2` is `4.0`. Second, `//` drops the fraction, giving only the whole-number part of the answer: `7 // 2` is `3`.

## Expressions

An **expression** is a combination of values, variables and operators that Python can work out to a single value. `4 + 3` is an expression. So is a lone `5`, or a variable name by itself.

```python
width = 6
height = 4
area = width * height
print(area)
print(width + height * 2)
```

The assignment line uses the expression `width * height`. Python calculates it, gets `24`, and stores that under `area`. The last line shows `14`, as we are about to explain.

When you type an expression in the interactive prompt, Python shows its value. In a file, nothing is shown unless you `print` it.

## Order of operations

When an expression has more than one operator, Python decides what to do first using rules similar to school maths. A common memory aid is **PEMDAS**:

1. **P**arentheses (brackets) first
2. **E**xponents (`**`)
3. **M**ultiplication and **D**ivision (including `//` and `%`), left to right
4. **A**ddition and **S**ubtraction, left to right

```python
print(2 + 3 * 4)       # 14, because 3 * 4 happens first
print((2 + 3) * 4)     # 20, because brackets go first
print(2 ** 3 * 2)      # 16, because 2 ** 3 is 8, then 8 * 2
print(10 - 4 - 3)      # 3, worked out left to right
```

When in doubt, add brackets. They cost nothing, and they make your meaning clear to the next reader, who might be you next week.

A classic trap is the average:

```python
print(10 + 20 / 2)     # 20.0, not 15.0
print((10 + 20) / 2)   # 15.0, the average
```

## The modulus operator

The **modulus** operator `%` gives the **remainder** after a division. The expression `17 % 5` asks: after taking away as many fives as you can from 17, what is left? The answer is `2`, because 17 is three fives plus 2.

```python
print(17 // 5)   # 3, how many whole fives
print(17 % 5)    # 2, what is left
```

`%` is more useful than it first appears.

- **Even or odd.** A number is even when `n % 2` is `0`.
- **Divisibility.** `n % 7 == 0` means n is a multiple of 7.
- **Clock arithmetic.** Starting at 9 o'clock, 5 hours later is `(9 + 5) % 12`, which is `2`.
- **Splitting a total.** 135 minutes is `135 // 60` hours and `135 % 60` minutes left over, so 2 hours 15 minutes.

## Mixing ints and floats

If an operation includes a `float`, the answer is a `float`. `3 + 0.5` is `3.5` and `2 * 1.5` is `3.0`. Python converts the whole number to a float for you.

## Common mistakes

- **Forgetting that multiplication needs a symbol.** Write `2 * x`, not `2x`.
- **Using `^` for power.** In Python `^` is something else entirely. Use `**`.
- **Not using brackets in an average.** `a + b / 2` is not `(a + b) / 2`.
- **Expecting `/` to give a whole number.** It always gives a float; use `//` when you want the whole part.
- **Confusing `//` and `%`.** `//` is "how many times", `%` is "what is left over".

## What to take away

1. Operators act on operands; an expression boils down to one value.
2. `/` gives a float, `//` the whole part, `%` the remainder, `**` the power.
3. Brackets first, then powers, then multiply and divide, then add and subtract.
4. `n % 2 == 0` is the classic even test; `//` and `%` together split totals into units.
