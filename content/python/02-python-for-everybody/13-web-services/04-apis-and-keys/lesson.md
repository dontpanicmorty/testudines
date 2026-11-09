+++
id = "everybody.web-services.apis-and-keys"
title = "Calling an API"
minutes = 30
+++

# Calling an API

So far you have parsed data that was handed to you as text. Now let's ask another computer for it.

## What an API is

An **Application Programming Interface** (API) is a set of rules for one program to ask another program for things. A **web API** is an API you reach through a web address, using the same HTTP requests a browser uses. You send a request, and the answer comes back as XML or JSON, ready for your program instead of for human eyes.

Splitting software into small services that talk through APIs is called **service-oriented design**. A bike-share company might run one service for station data and another for payments. Each can change inside, as long as its API stays the same.

## Building the request address

Most APIs take their questions in the **query string**: the part of the address after a `?`, made of `name=value` pairs joined with `&`.

```
https://api.example.test/stations?zone=North&limit=5
```

Do not glue strings by hand. Spaces and symbols like `&` must be escaped, or they will break the address. `urllib.parse.urlencode` does it correctly:

```python
from urllib.parse import urlencode

params = {"zone": "North Quay", "limit": 5, "q": "bikes & docks"}
query = urlencode(params)
print(query)
# zone=North+Quay&limit=5&q=bikes+%26+docks

url = "https://api.example.test/stations" + "?" + query
```

## Fetching and parsing the answer

`urllib.request.urlopen(url)` sends the request and returns a response you can read. `.read()` gives **bytes**, so decode them to text, then parse.

```python
import json
from urllib.request import urlopen

def fetch_json(url):
    with urlopen(url, timeout=5) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)
```

The `with` block closes the connection for you. The `timeout` stops your program waiting forever if the other computer is silent.

Testudines works offline, so the exercises start a tiny server on your own machine (`127.0.0.1`) and call that. Your code is the same as it would be for a real service.

## Pages of results

Services rarely send everything at once. A typical JSON answer includes a link to the next page:

```json
{"items": [1, 2, 3], "next": "http://127.0.0.1:8000/page2"}
```

Loop until `next` is `null`, collecting items as you go.

## API keys and rate limits

Many services want to know who is calling. They give you an **API key**: a long secret string you add to each request, often as a parameter like `key=...`. Keys let the service count your usage and block misuse.

Services also set **rate limits**, such as "100 requests per hour". If you go over, you get an error response (often status 429) and may be blocked. Be polite: fetch only what you need, save answers so you do not ask twice, and pause between requests with `time.sleep`.

## Keeping keys out of your code

A key typed into your program is easy to leak: you share the file, post it online, and now anyone can spend your allowance. Instead, keep the key outside the code. One common way is an **environment variable**:

```python
import os

key = os.environ.get("BIKE_API_KEY")
if key is None:
    raise RuntimeError("Set BIKE_API_KEY before running")
```

Another is a separate config file that you never share. Either way, the source stays safe to publish.

## OAuth in concept

Some services act on behalf of a person, such as reading their account. For those, a bare key is not enough. **OAuth** is a standard where the person approves your program on the service's own site, and the service hands your program a short-lived **token**. Requests are then **signed**: a calculation using your secret and the request details produces a signature that proves the request is genuine without sending the secret itself. Libraries usually do the signing for you. The idea to remember is: secrets are used to prove identity, and they never appear in plain sight.

## Common mistakes

- Building a query string with `+` and forgetting to escape characters.
- Forgetting `.decode()` and trying to parse bytes as text (`json.loads` does accept bytes, but XML and string handling are easier after decoding).
- Putting an API key straight into code that you share.
- Calling an API in a tight loop and hitting the rate limit.
- Not setting a `timeout`.
