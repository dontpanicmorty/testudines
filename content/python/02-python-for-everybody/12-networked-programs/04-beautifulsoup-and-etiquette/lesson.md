+++
id = "everybody.networked-programs.beautifulsoup-and-etiquette"
title = "BeautifulSoup and scraping etiquette"
minutes = 30
+++

# BeautifulSoup and scraping etiquette

The last lesson showed that patterns struggle with real HTML. A better way is to use a library that understands HTML the way a browser does. One that comes with this course is **BeautifulSoup**, from the package `bs4`.

> **Offline note.** URLs like `http://example.org/` are examples only. The exercises run against a small server on your own computer.

## Making a soup

```python
from bs4 import BeautifulSoup

html = """
<html><head><title>Garden club</title></head>
<body>
  <h1>Welcome</h1>
  <p>Read our <a href="/news.html">news</a> or visit
     <a href='http://example.org/maps' class="out">the map</a>.</p>
  <img src="/tulip.png" alt="A tulip">
</body></html>
"""
soup = BeautifulSoup(html, "html.parser")
```

`BeautifulSoup(text, "html.parser")` reads the HTML and builds a tree of tags. The second argument says which reader to use; `"html.parser"` is built into Python.

## Finding tags

```python
print(soup.title)              # <title>Garden club</title>
print(soup.title.string)       # Garden club
print(soup.h1.get_text())      # Welcome
```

`soup.title` is the first `<title>` tag. `.string` or `.get_text()` gives the text inside a tag, without the angle brackets.

`soup.find_all("a")` returns a **list** of every `<a>` tag, in page order. `soup.find("a")` returns only the first, or `None` if there is none.

```python
for tag in soup.find_all("a"):
    print(tag.get_text(), "->", tag.get("href"))
```

Output:

```
news -> /news.html
the map -> http://example.org/maps
```

Notice that the single quotes and the extra `class` attribute caused no trouble at all. That is the big advantage over a regular expression.

## Attributes

A tag works a little like a dictionary of its attributes.

```python
link = soup.find("a")
print(link["href"])          # /news.html
print(link.get("class"))     # None: this link has no class
print(link.get("class", "none"))
```

Use `tag.get("name")` when the attribute may be missing: it gives `None` (or a default you supply) instead of a `KeyError`. Careful: an `<a>` tag without `href` exists in real pages, so always use `.get`.

Images work the same way:

```python
for img in soup.find_all("img"):
    print(img.get("src"), img.get("alt"))
```

You can also filter by attribute. `soup.find_all("a", href=True)` returns only the anchors that have an `href`.

## Tables

A table is `<table>`, with a `<tr>` for each row and `<td>` (or `<th>` for headers) for each cell.

```python
rows = []
for tr in soup.find_all("tr"):
    cells = [cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])]
    rows.append(cells)
```

`get_text(strip=True)` removes spaces and line breaks around the text. Passing a list of names to `find_all` matches any of them.

## Being a good citizen: scraping etiquette

A program can fetch pages far faster than any person. That brings responsibilities.

- **Terms of use.** Many sites state what automated access is allowed. Read them. Some forbid scraping altogether.
- **robots.txt.** Most sites publish a plain text file at `/robots.txt`, such as `http://example.org/robots.txt`. It lists areas they ask robots not to visit:

```
User-agent: *
Disallow: /private/
Disallow: /admin
```

`User-agent: *` means "this applies to every robot". Each `Disallow` line gives a path prefix to stay out of. A polite program fetches this file first and obeys it.
- **Go slowly.** Add a pause between requests (`time.sleep(1)`) so you do not overload a small server.
- **Identify yourself** and avoid scraping personal data.
- **Prefer an official data source.** If the site offers a download or an API, use that instead of scraping.
- **Respect copyright.** Being able to fetch something does not mean you may republish it.

Checking a path against the rules is a small job: for each `Disallow` line, a path is off limits if it starts with that prefix.

## Debugging with soup

- Print `soup.prettify()` to see the tree with neat indentation.
- Print `len(soup.find_all("a"))` to see how many matches you really got.
- If `find` gives `None` and you use it anyway, you get `AttributeError: 'NoneType' object has no attribute ...`. Check first.
- Some pages build their content with JavaScript after loading. The HTML you fetch then lacks it, and no parser can find what is not there.

## Common mistakes

- Using `tag["href"]` on a tag with no `href` instead of `tag.get("href")`.
- Forgetting that `find_all` returns a list and `find` returns one tag or `None`.
- Hammering a server with requests in a fast loop.
- Ignoring `robots.txt` and the site's terms.
