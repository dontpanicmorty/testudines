+++
id = "everybody.functions.defining-functions"
title = "Defining your own functions"
minutes = 25
+++

# Defining your own functions

Python's built-in functions are handy, but the real power comes when you write your own. A function lets you give a name to a few lines of code and use it again and again.

## Your first function

You create a function with the keyword `def`, short for "define":

```python
def say_welcome():
    print("Welcome aboard")
    print("Please take a seat")
```

Let us go through it:

- `def` starts the definition.
- `say_welcome` is the function's name. The rules are the same as for variable names.
- The brackets `()` come next; they will hold parameters in a moment.
- The line ends with a **colon**.
- The lines below are the **body**. They are indented, as they were with `if`.

Writing this does *not* run the code. It only teaches Python the new function. To run it, you **call** it:

```python
say_welcome()
say_welcome()
```

This displays the two lines twice, because we called the function twice.

## Definitions and uses

Every function has two sides: the **definition** (the `def` block) and the **uses** (the calls). Python must see the definition before it reaches a call, because it reads from top to bottom.

```python
greet()          # fails: greet is not defined yet

def greet():
    print("Hi")
```

This stops with a `NameError`. Put the `def` first and it works.

## Flow of execution

The order in which Python runs statements is the **flow of execution**. It starts at the top of the program and works down, one statement at a time.

A function definition does not change that flow: Python reads the definition, remembers it, and moves on. The body is skipped until the function is called. At a call, the flow jumps to the body, runs all of it, and then returns to the line just after the call.

```python
def announce():
    print("2. inside the function")

print("1. before the call")
announce()
print("3. after the call")
```

The lines are displayed in order 1, 2, 3, because the call to `announce` took a detour into the body and came back.

A function can call other functions, so the flow can nest several levels deep. Python always remembers where to go back to.

## Parameters and arguments

Functions become more useful when you can give them information. A **parameter** is a variable name listed in the brackets of the definition. An **argument** is the actual value you pass when you call the function.

```python
def welcome(name):
    print("Welcome,", name)

welcome("Aisha")
welcome("Ben")
```

This shows `Welcome, Aisha` then `Welcome, Ben`. When you call `welcome("Aisha")`, Python stores `"Aisha"` in the parameter `name`, then runs the body. In the second call, `name` holds `"Ben"`.

A function can take several parameters, separated by commas. Arguments are matched by position:

```python
def show_total(price, quantity):
    print("Total:", price * quantity)

show_total(2.5, 4)
```

This shows `Total: 10.0`. The first argument went into `price` and the second into `quantity`.

An argument can be a value, a variable or any expression:

```python
cost = 3
show_total(cost + 1, 2 * 5)
```

Python works out each argument first, then runs the function.

## Local variables

Names created inside a function, including its parameters, exist only while the function runs. They are **local** to the function. Code outside cannot see them.

```python
def double(number):
    result = number * 2
    print(result)

double(4)
print(result)
```

The first `print` inside the function works. The last line fails with a `NameError`, because `result` is local to `double`. Local names also mean you can reuse a name like `result` in many functions without them interfering.

## Common mistakes

- **Forgetting the brackets in a call.** `say_welcome` alone does nothing; `say_welcome()` runs it.
- **Calling a function before it is defined.**
- **Forgetting the colon** after the `def` line, or forgetting to indent the body.
- **Passing the wrong number of arguments.** Python complains with a `TypeError` that tells you how many it expected.
- **Mixing up the order of arguments.** They match parameters by position.
- **Expecting a variable made inside a function to be available outside.**

## What to take away

1. `def name(parameters):` followed by an indented body defines a function; calling it runs the body.
2. Python runs the file top to bottom; a call jumps into the body and then comes back.
3. Parameters are the names in the definition; arguments are the values you pass.
4. Names created inside a function are local to it.
