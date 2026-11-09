+++
id = "everybody.variables-expressions-statements.values-types-variables"
title = "Values, types and variables"
minutes = 25
+++

# Values, types and variables

Programs work with data. In this lesson you meet the basic kinds of data Python understands and learn how to give your data names.

## Values and types

A **value** is a piece of data, such as the number `42` or the text `"tea"`. Every value has a **type**, which says what kind of thing it is and what you can do with it.

Three types will cover most of your first programs:

- `int`, a whole number: `7`, `-3`, `1000`
- `float`, a number with a decimal point: `2.5`, `-0.1`, `3.0`
- `str` (short for string), text: `"tea"`, `'hello'`, `"42"`

You can ask Python for the type of any value with `type`:

```python
print(type(7))
print(type(2.5))
print(type("tea"))
```

This shows `<class 'int'>`, `<class 'float'>` and `<class 'str'>`.

Text must be surrounded by quotation marks, either single (`'`) or double (`"`). That is how Python tells a word from a name or a number. Notice that `"42"` in quotes is text, not a number: you cannot do arithmetic on it. `type("42")` is `str`.

```python
print(type(3.0))      # float, because of the decimal point
print(type("3.0"))    # str, because of the quotes
```

## Variables

A **variable** is a name that refers to a value. Think of a label stuck on a jar. You create one with an **assignment statement**, which uses a single equals sign:

```python
cups = 3
drink = "tea"
price = 1.75
```

Read `cups = 3` as "let `cups` be 3" or "`cups` now refers to 3". It does **not** mean "cups equals 3" like in maths. The thing on the left is the name; the value on the right is stored under it.

Once a variable exists you can use its name anywhere you could use the value:

```python
print(cups)
print(cups + 2)
print(type(drink))
```

This shows `3`, then `5`, then `<class 'str'>`.

Variables can be changed. Assign again and the label moves to a new value:

```python
cups = 3
cups = 10
print(cups)
```

Only `10` is shown. The old value is forgotten. You can even use the old value to make the new one:

```python
cups = cups + 1
```

This takes the current value of `cups`, adds 1, and stores the result back under the name `cups`.

Values and variables are different things. A variable keeps its type from the value it points at, so a name pointing at a number can later point at text. Python does not mind.

## Variable names and keywords

You can choose almost any name, with a few rules:

- Names can contain letters, digits and underscores (`_`).
- Names cannot start with a digit: `2cups` is illegal, `cups2` is fine.
- Names are case sensitive: `Tea`, `tea` and `TEA` are three different variables.
- Spaces are not allowed. Use an underscore instead: `cups_of_tea`.
- You cannot use a **keyword**, one of Python's reserved words such as `class`, `if` or `while`.

If you break a rule, Python shows a `SyntaxError`:

```python
2cups = 3         # starts with a digit
my tea = "green"  # contains a space
class = "first"   # reserved word
```

## Statements

A **statement** is an instruction that Python carries out. So far you have seen two kinds: `print(...)` statements and assignment statements. When you run a program, Python goes through the statements in order.

An assignment statement does not display anything. It just stores a value. If you want to see a value, `print` it.

```python
width = 4
height = 3
print(width)
```

Only one thing is shown: `4`. The assignments happen silently.

## Common mistakes

- **Writing `=` when you mean "is equal to".** A single `=` always means "store". Comparing comes in chapter 3.
- **Putting a number in quotes.** `"42"` is text; `42` is a number.
- **Using a variable before giving it a value.** This gives a `NameError`.
- **Using the wrong capital letter.** `Cups` and `cups` are different names.
- **Using a name with a space or a hyphen.** `my-tea` looks like "my minus tea".

## What to take away

1. Values have types: `int`, `float` and `str` for starters.
2. `name = value` stores a value under a name; assigning again replaces it.
3. Variable names use letters, digits and underscores, cannot start with a digit and cannot be keywords.
4. A statement is one instruction; assignments store, `print` shows.
