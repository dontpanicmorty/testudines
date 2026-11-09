+++
id = "everybody.networked-programs.scraping-html-with-regex"
title = "Reading HTML with regular expressions"
minutes = 25
+++

# Reading HTML with regular expressions

Most web pages are written in **HTML** (HyperText Markup Language). HTML wraps content in **tags** that tell the browser what each part is. **Web scraping** means having a program read a page and pull out the pieces you need: the links, the headings, the prices.

> **Offline note.** Addresses such as `http://example.org/` here are only illustrations. The exercises serve their own pages from a tiny server on your computer.

## What HTML looks like

```html
<html>
  <head><title>Garden club</title></head>
  <body>
    <h1>Welcome</h1>
    <p>Read our <a href="/news.html">news</a> or visit
       <a href="http://example.org/maps">the map</a>.</p>
    <img src="/tulip.png" alt="A tulip">
  </body>
</html>
```

- A tag is written in angle brackets: `<p>` opens a paragraph, `</p>` closes it.
- Tags can have **attributes**, written `name="value"` inside the opening tag. Here `href` holds a link's address and `src` an image's address.
- Tags nest inside each other like boxes.

## Fetching the page

First get the page text with `urllib`, as in the last lesson.

```python
import urllib.request

with urllib.request.urlopen(url) as response:
    html = response.read().decode("utf-8")
```

From here on, `html` is just a long string, so any string tool works on it.

## Finding links with a pattern

A link is `<a href="...">`. The address sits between the quotes. A non-greedy group extracts it.

```python
import re

links = re.findall(r'href="(.*?)"', html)
print(links)    # ['/news.html', 'http://example.org/maps']
```

Reading the pattern: the literal text `href="`, then a group catching as little as possible, then the closing quote. Non-greedy matters: a greedy `.*` would run to the last quote on the line.

To find only links that start with `http`:

```python
web_links = re.findall(r'href="(http[^"]*)"', html)
```

`[^"]*` means "any number of characters that are not a quote", a safer alternative to `.*?`.

## Finding text between tags

To get the text inside every heading, capture between the opening and closing tags.

```python
headings = re.findall(r"<h1>(.*?)</h1>", html)
print(headings)    # ['Welcome']
```

## Why regular expressions are fragile for HTML

This works on tidy pages and breaks easily on real ones. All of these mean the same thing to a browser but not to our pattern:

```html
<a href='/news.html'>      single quotes
<A HREF="/news.html">      capital letters
<a class="big" href="/news.html">   another attribute first
<a
   href="/news.html">      a line break inside the tag
```

You can patch the pattern for each case, with options like `re.IGNORECASE`, but the patterns get long and still miss things. Also, a page can contain a tag inside a comment or in a script, which a browser ignores but a pattern happily finds.

A rule of thumb: patterns are fine for a **quick, one-off** job on a page you have looked at and understand. For anything you want to rely on, use a real HTML reader. The next lesson introduces one.

## Case-insensitive matching

You can tell a pattern to ignore capitals with a flag:

```python
re.findall(r'href="(.*?)"', html, re.IGNORECASE)
```

This also matches `HREF="..."`, though it does not fix the other problems above.

## Debugging scrapers

- Save the page to a file or print its first 500 characters. Look at the real HTML, not at what you see in a browser; they can differ a lot.
- Print `len(html)`. A tiny length often means you fetched an error page or a "please log in" page.
- Test your pattern on a small piece of HTML you paste into a variable.
- If the list is empty, check quotes: the page might use single quotes.

## Common mistakes

- Using a greedy `.*` so that one match swallows several tags.
- Forgetting the `r` prefix on the pattern.
- Expecting a pattern to cope with every style of writing a tag.
- Fetching with `.read()` and forgetting to `.decode()` before using `re` with a string pattern. Mixing bytes and strings raises a `TypeError`.
