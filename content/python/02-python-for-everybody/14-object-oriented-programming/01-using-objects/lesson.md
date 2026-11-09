+++
id = "everybody.object-oriented-programming.using-objects"
title = "Everything is an object"
minutes = 25
+++

# Everything is an object

A short program fits in your head. A long one does not. When a program grows to hundreds of lines, you need ways to break it into pieces so you only think about one piece at a time. You already know one way: functions. This chapter adds another: **objects**.

## You have been using objects all along

An **object** is a bundle of two things: some **data**, and some **actions** that work on that data. The actions are called **methods**. A method is just a function that belongs to an object, and you call it with a dot.

```python
word = "harbour"
print(word.upper())      # HARBOUR
print(word.count("a"))   # 2

shelf = ["tide", "moss"]
shelf.append("reed")
print(shelf)             # ['tide', 'moss', 'reed']
```

`word` is a string object, and `.upper()` is a method that string objects have. `shelf` is a list object, and `.append()` is a list method. Numbers, dictionaries, files and even functions are objects too. In Python, everything is an object.

## What type is it?

Every object has a **type**, which says what kind of thing it is and which methods it has. Ask with `type()`:

```python
print(type(word))     # <class 'str'>
print(type(shelf))    # <class 'list'>
print(type(3.5))      # <class 'float'>
print(type(None))     # <class 'NoneType'>
print(type(word).__name__)   # str
```

`type(x).__name__` gives just the short name as a string, which is handy in messages.

## What can it do? dir()

Not sure which methods an object has? Ask with `dir()`. It returns a list of names.

```python
names = dir(shelf)
print(names[-3:])   # ['remove', 'reverse', 'sort']
```

You will see many names that start and end with double underscores, like `__len__`. These are Python's own plumbing, so ignore them for now. Names without underscores are the methods you call yourself. Pair `dir()` with `help(str.upper)` to read what a method does.

```python
public = [n for n in dir(word) if not n.startswith("_")]
print(public[:4])   # ['capitalize', 'casefold', 'center', 'count']
```

## Programs have a shape: input, processing, output

Before you split a program into pieces, notice that most programs do three jobs in order:

1. **Input**: get the data (read a file, parse a response).
2. **Processing**: work out the answer (count, filter, total).
3. **Output**: present it (print, write a file, build a report string).

Here is a small program laid out that way, with one function per job:

```python
def read_sightings(text):
    rows = []
    for line in text.splitlines():
        bird, count = line.split(",")
        rows.append((bird, int(count)))
    return rows

def total_by_bird(rows):
    totals = {}
    for bird, count in rows:
        totals[bird] = totals.get(bird, 0) + count
    return totals

def format_report(totals):
    return "\n".join(f"{b}: {n}" for b, n in sorted(totals.items()))

log = "wren,2\nheron,1\nwren,3"
print(format_report(total_by_bird(read_sightings(log))))
```

This prints `heron: 1` and `wren: 5`. Each function is small, testable alone, and has one clear purpose.

## Subdividing a problem into objects

Functions split a program by *actions*. Objects split it by *things*. If you were tracking library loans, the things in the story would be members, books and loans. Each thing keeps its own data and knows how to do its own jobs: a book knows its title, a member knows how many books they hold. Instead of passing loose dictionaries from function to function, you ask each object to do its own work.

To decide on objects, read your problem description and underline the nouns. Many of them become objects. The verbs become their methods. In the next lesson you will build your own.

## Common mistakes

- Forgetting the parentheses: `word.upper` is the method itself, `word.upper()` runs it.
- Expecting every type to share methods: strings have `.upper()`, lists do not.
- Reading all of the output of `dir()`. Filter out names starting with `_`.
- Mixing input, processing and output in one long function, which makes it hard to test.
