+++
id = "everybody.dictionaries.counting-words-in-files"
title = "Counting words in a file"
minutes = 30
+++

# Counting words in a file

Now we put dictionaries to work on real text. The plan: read a file line by line, split each line into words, and count each word with the `.get()` pattern. Then we will clean the words up so that "Tea", "tea" and "tea." all count as the same word.

## Step one: the plain version

Imagine a file `notes.txt` containing:

```
the tea is hot
the cup is cold
```

This program counts its words.

```python
counts = {}
with open("notes.txt") as handle:
    for line in handle:
        words = line.split()
        for word in words:
            counts[word] = counts.get(word, 0) + 1
print(counts)
```

What it does, piece by piece:

- `with open(...) as handle` opens the file and closes it again for you.
- `for line in handle` gives one line at a time.
- `line.split()` with no argument breaks the line at any run of spaces or tabs and throws away the newline. `"the tea is hot\n".split()` gives `['the', 'tea', 'is', 'hot']`.
- The inner loop counts each word.

The result is `{'the': 2, 'tea': 1, 'is': 2, 'hot': 1, 'cup': 1, 'cold': 1}`.

If you already have the text in a variable instead of a file, the loop over `text.splitlines()` does the same job. The exercises build their own text files, so you will always be given a path.

## The problem with real text

Real writing has capital letters and punctuation. Look at this line:

```
Tea, tea! TEA?
```

The plain program sees `Tea,`, `tea!` and `TEA?`: three different "words", each counted once. We want one word, `tea`, counted three times. We need two clean-up steps.

## Step two: lowercase everything

`line.lower()` returns a copy of the line in small letters. Do it before splitting.

```python
line = "Tea, tea! TEA?"
print(line.lower())    # tea, tea! tea?
```

## Step three: remove punctuation

Python keeps a handy string of punctuation characters in the `string` module.

```python
import string
print(string.punctuation)    # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
```

To delete characters from a string we use `translate()`. It needs a **translation table**, which we make with `str.maketrans()`. With three arguments, the third one lists characters to delete.

```python
import string

table = str.maketrans("", "", string.punctuation)
print("tea, tea! tea?".translate(table))    # tea tea tea
```

The first two arguments (`""` and `""`) say "do not swap any characters for others". The third says "remove every one of these". Make the table once, before the loop, and reuse it.

## Putting it together

```python
import string

table = str.maketrans("", "", string.punctuation)
counts = {}
with open("notes.txt") as handle:
    for line in handle:
        line = line.lower().translate(table)
        for word in line.split():
            counts[word] = counts.get(word, 0) + 1
```

Each line is lowercased, stripped of punctuation, split, and counted.

One side effect to know about: removing punctuation turns `don't` into `dont`, and `well-known` into `wellknown`. That is a good enough rule for counting, but you should know it is a choice.

## Looking at the result

To print the counts alphabetically, loop over `sorted(counts)`. To find the most frequent word, use the "best so far" loop from the last lesson.

## Debugging with small inputs

Reading a huge file and getting wrong numbers is hard to fix. Make a tiny file of two or three lines whose answers you know, run the program on it, and compare. Print `counts` after the first line. When the tiny file works, try bigger ones.

Useful sanity checks: the counts must add up to the total number of words, and no key should contain capital letters or punctuation after cleaning.

## Common mistakes

- Cleaning after splitting only some of the words, or forgetting to reassign: `line.lower()` alone does nothing, because strings cannot be changed. Write `line = line.lower()`.
- Passing the characters in the wrong place: `str.maketrans(string.punctuation)` fails. The deleting characters are the **third** argument.
- Building the translation table inside the loop. It works but wastes effort.
- Opening a file that is in a different folder from your program, which gives `FileNotFoundError`.
