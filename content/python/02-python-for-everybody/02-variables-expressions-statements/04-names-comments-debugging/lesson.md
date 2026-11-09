+++
id = "everybody.variables-expressions-statements.names-comments-debugging"
title = "Good names, comments and debugging"
minutes = 20
+++

# Good names, comments and debugging

Writing code that works is the first goal. Writing code that you can still read next month is the second. This lesson is about habits that make programs easier to understand and fix.

## Choosing mnemonic variable names

**Mnemonic** (say it "nem-ON-ik") means "helping you remember". A mnemonic variable name tells the reader what the variable holds.

Compare these two programs. They do exactly the same thing:

```python
a = 35
b = 12.5
c = a * b
print(c)
```

```python
hours_worked = 35
hourly_rate = 12.5
weekly_pay = hours_worked * hourly_rate
print(weekly_pay)
```

Python does not care which you write. People do. The second program explains itself, and if the answer looks wrong, you can see at a glance which line to check.

Some guidelines:

- Use lowercase words joined with underscores: `total_price`, `number_of_tickets`.
- Make names long enough to be clear, short enough to type. `tax` or `tax_rate` beats `t` or `the_amount_of_tax_that_we_apply`.
- Avoid names that look alike, such as `l` (lower-case L) and `1`, or `O` and `0`.
- Do not name variables after built-in functions like `type`, `max` or `sum`. It works, but you lose the original function.
- Use a noun for a value (`price`) and save verbs for things that do actions.

## Writing comments

A comment starts with `#`. It is a note to the reader that Python ignores.

```python
# Pay is overtime-free for now
weekly_pay = hours_worked * hourly_rate
```

Good comments explain the reason for something, or summarise a tricky block. Bad comments repeat the code:

```python
x = x + 1    # add one to x
```

That tells the reader nothing new. Better still, choose good names and write simple lines so you need fewer comments.

Another use is temporarily switching off a line while you test: put `#` in front of it. This is called "commenting out".

## Debugging in this chapter

You have met `SyntaxError`, `NameError` and `TypeError`. Variables and expressions bring a few typical failures.

**Illegal name.** Python complains straight away about names that break the rules. Check for spaces, a leading digit or a reserved word.

**Wrong variable name.** `NameError: name 'hours_worked' is not defined` often just means a typo, such as `hours_woked` on a later line. Compare the spelling in both places.

**Wrong order.** Use a variable before it has a value and you get a `NameError`, because Python reads from top to bottom.

**Wrong type.** `TypeError: can only concatenate str (not "int") to str` means you tried to add text and a number. Convert one of them.

**Wrong calculation.** There is no error message, just a wrong answer. Remember the order of operations. If `total + tax / 100` looks wrong, ask whether brackets are missing. Print the in-between values to see where things go off:

```python
price = 80
tax_percent = 20
tax = price * tax_percent / 100
print(tax)                      # check this step: 16.0
total = price + tax
print(total)
```

**Rounding surprises.** Floating point numbers cannot always store a decimal exactly. `0.1 + 0.2` gives `0.30000000000000004`. It is not a bug; it is how computers store decimals. When comparing floats, check that they are *close* rather than exactly equal.

## A worked example

Suppose a program should work out the price per slice of a pizza.

```python
pizza_price = 12
slices = 8
price_per_slice = pizza_price / slices
print(price_per_slice)
```

It shows `1.5`. To check, multiply back: 1.5 times 8 is 12. Good. Now suppose someone writes `pizza_price / slices * 2` by mistake; the answer, 3.0, looks plausible but is wrong. Always have a rough idea of the answer before you run the program. Even a quick sanity check catches many mistakes.

## Common mistakes

- **One-letter names everywhere.** `x`, `y` and `z` are fine in a quick experiment but hard to follow in a longer program.
- **Comments that disagree with the code.** If you change a line, change its comment too, or delete it.
- **Reusing one variable for two different things.** Give each idea its own name.
- **Trusting a number that "looks about right".** Calculate one example by hand.
- **Changing the program without re-running it.** Run after every small change.

## What to take away

1. Mnemonic names tell the reader what a variable holds.
2. Comments explain why, not what; they are ignored by Python.
3. Use the error message type to guess the cause: name, type, order or calculation.
4. Print intermediate values and check one example by hand.
