+++
id = "everybody.why-program.talking-to-python"
title = "Talking to Python"
minutes = 25
+++

# Talking to Python

Python has a small vocabulary and a few simple rules for building sentences. Learn both and you can start giving instructions.

## Words Python already knows

Python reserves some words for its own use. These **reserved words** (also called **keywords**) have a fixed meaning, and you cannot use them as names for your own things. Examples are `if`, `else`, `for`, `while`, `def`, `return`, `True`, `False` and `import`.

You can ask Python for the full list:

```python
import keyword
print(keyword.kwlist)
print(keyword.iskeyword("while"))
print(keyword.iskeyword("banana"))
```

The first `print` shows every reserved word. The next two show `True` and `False`: `while` is reserved, `banana` is not. Everything that is not reserved, such as names you make up, is yours to define.

## Sentences

A line of Python that does something is a **statement**, a bit like a sentence. Statements have to follow the rules exactly, including spelling, brackets and quotation marks. Computers are strict readers; a missing bracket is not "close enough".

```python
print("Meet at noon")
print(3 + 4)
```

The first line displays text. The second does a calculation and displays the answer `7`. Text goes inside quotation marks; numbers do not.

## The interactive prompt

You can try Python one line at a time, like a conversation. When you start Python's interactive mode, it shows a prompt that looks like `>>>`. You type a line, press Enter, and Python replies straight away.

```python
>>> 6 * 7
42
>>> print("Ready")
Ready
>>> "ab" + "cd"
'abcd'
```

This is a great place to experiment, because mistakes cost nothing. The downside is that nothing is saved. When you close it, your lines are gone.

## Interpreters and compilers

The computer's CPU cannot read Python directly. Something has to translate. There are two ways to do it.

- A **compiler** reads your whole program first and turns it into a separate file of machine instructions, which you then run.
- An **interpreter** reads your program and carries out the instructions directly, one at a time.

Python is usually used with an interpreter. The interpreter is itself a program called `python`. It is what shows the `>>>` prompt, and it is what runs your files.

## Writing a program file

To keep your work, save the lines in a text file. Python files end in `.py`. Here is a small one called `trip.py`:

```python
print("Planning the trip")
print(120 / 4)
print("Done planning")
```

You run it from a terminal with `python trip.py`, and it prints three lines in order. In Testudines, the Run button does that for you.

## What a program is

A program is a series of statements, written to do one useful job. The same few building blocks appear in every program, from the smallest to the largest:

- **Input.** Get data from the outside world: a keyboard, a file, the network.
- **Output.** Show or save results.
- **Sequential execution.** Run statements one after another, top to bottom.
- **Conditional execution.** Check something and run some statements only if it is true.
- **Repeated execution.** Do something again and again, often with small changes.
- **Reuse.** Write a set of steps once, give it a name, and use it as often as you like.

Here is a glimpse of all of them in action. You do not need to follow every detail yet, only the idea:

```python
name = input("Your name? ")        # input
if name == "":                     # conditional execution
    name = "stranger"
for count in range(3):             # repeated execution
    print("Hello,", name)          # output
```

Each of these blocks gets its own lesson later in the course.

## Order matters

Python reads a file from top to bottom. If a statement uses something that has not been created yet, it fails.

```python
print(price)
price = 5
```

This stops with an error because `price` does not exist yet when the first line runs. Swap the lines and it works.

## Common mistakes

- **Forgetting the quotation marks** around text, or using only one of the pair. `print("Hi)` fails.
- **Using a reserved word as a name**, for example calling something `class` or `if`.
- **Writing a capital letter by accident.** Python treats `Print` and `print` as different words.
- **Expecting the interactive prompt to remember.** Save longer work in a file.
- **Copying the `>>>` prompt** into a file. It is only a signal that Python is waiting; do not type it.

## What to take away

1. Reserved words belong to Python; the rest of the names are yours.
2. A statement is one instruction. `print(...)` displays things.
3. The interactive prompt is for quick experiments; files are for keeping programs.
4. Python uses an interpreter, which carries out your program directly.
5. Programs are made from input, output, sequence, conditions, repetition and reuse.
