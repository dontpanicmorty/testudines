+++
id = "everybody.functions.why-functions-and-debugging"
title = "Why functions? Building and debugging programs"
minutes = 20
+++

# Why functions? Building and debugging programs

By now you know how to write functions. This lesson explains why they are worth the effort, how to combine them, and how to debug code that uses them.

## Why use functions?

Programmers write functions for several good reasons.

- **Naming a group of statements** makes a program easier to read. `calculate_total()` tells you more than ten lines of arithmetic.
- **Avoiding repetition.** If you need the same steps in three places, write them once as a function and call it three times. When you spot a mistake, you fix it in one place only.
- **Breaking a big problem into small parts.** You can write and test each part separately, then combine them.
- **Reuse.** A well-written function can be copied into a future program, or shared; that is how modules like `math` came to exist.

Compare these two ways to show two price tags:

```python
print("Price:", round(19.99 * 1.2, 2))
print("Price:", round(5.5 * 1.2, 2))
```

```python
def with_vat(price):
    return round(price * 1.2, 2)

print("Price:", with_vat(19.99))
print("Price:", with_vat(5.5))
```

The second one gives the 20 percent tax calculation a name. If the tax rate changes, you edit one line.

## Functions that call functions

A function body can call other functions, including your own. This is how you build big things from small ones.

```python
def with_vat(price):
    return round(price * 1.2, 2)

def with_delivery(price):
    return price + 4

def final_price(price):
    return with_delivery(with_vat(price))

print(final_price(10))
```

Python works from the inside out: `with_vat(10)` gives `12.0`, then `with_delivery(12.0)` gives `16.0`. It shows `16.0`.

Each function does one small, clear job. If the final price is wrong, you can test `with_vat` and `with_delivery` separately to find which one is at fault.

## Designing a function

A friendly way to write one:

1. **Say what it does** in one sentence. If that is hard, the function probably does too much.
2. **Decide the inputs and the output.** What parameters does it need, and what should it return?
3. **Write the simplest version** and try it with an easy example.
4. **Try awkward cases**: zero, negative numbers, empty text.
5. **Tidy up** names and remove repeated code.

You can also add a short note under the `def` line, called a **docstring**, that explains the function. It is a text in triple quotes:

```python
def with_vat(price):
    """Return the price with 20 percent tax added."""
    return round(price * 1.2, 2)
```

## Debugging with functions

When a program with functions goes wrong, work through these checks.

- **Did the function run at all?** Add a `print` as the first line of the body. If nothing appears, the function was never called, perhaps because you forgot the brackets.
- **Are the arguments what you think?** Print the parameters at the top of the function.
- **What exactly was returned?** Store the result in a variable and print it. If it is `None`, a `return` is missing.
- **Order of arguments.** `describe("Priya", 30)` is not the same as `describe(30, "Priya")`.
- **Wrong number of arguments.** The `TypeError` message states how many the function expected.
- **A name that exists only inside.** If a `NameError` mentions a variable you created in a function, you are using it outside.
- **Test each function alone** with easy numbers before you test the whole program.

Here is a buggy example and how to find the problem:

```python
def percent_off(price, percent):
    discount = price * percent / 100
    price - discount

print(percent_off(50, 10))
```

This prints `None`. The last line of the function works out the new price, but has no `return`, so the result is thrown away. The fix is `return price - discount`.

## Common mistakes

- **Writing a long function that does everything.** Split it up.
- **Copying code instead of using a function.** Fixes then need to be repeated.
- **Not testing small parts first.**
- **Changing the function but not the calls.** If you add a parameter, update every call.
- **Leaving debugging `print` statements in** when the program is finished. Remove them.

## What to take away

1. Functions name steps, remove repetition, split big problems and can be reused.
2. Functions can call other functions; build big results from small ones.
3. Design with one clear sentence, simple inputs and outputs, and awkward test cases.
4. When debugging, check the function ran, the arguments, and what it returned.
