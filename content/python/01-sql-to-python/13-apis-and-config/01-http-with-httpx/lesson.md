+++
id = "apis-and-config.http-with-httpx"
title = "HTTP with httpx, without a network"
minutes = 25
+++

# HTTP with httpx, without a network

You already know request/response from the warehouse side: a query goes in, a result set or an error comes out. An HTTP API is the same contract over a different wire. You send a **method + URL (+ headers, body)**, you get back a **status code + headers + body**. Most data-engineering API work is: ask for JSON, check the status, parse, handle the failure cases.

> **Snowflake bridge.** A REST call is like `COPY INTO` from an external stage: the interesting parts are not the happy path but what happens when it is slow, partial, or rejected.

In this course nothing touches a real network. `httpx` lets us plug in a **transport**, an object that answers requests. `httpx.MockTransport` takes a plain function, so we can script any server behaviour and test it deterministically.

## A request and a response

```python
import httpx

def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"id": 1, "name": "Ada"})

client = httpx.Client(
    transport=httpx.MockTransport(handler),
    base_url="https://api.example.test",
)
resp = client.get("/users/1")
print(resp.status_code)
print(resp.json())
print(resp.headers["content-type"])
```

The `handler` receives the `Request` and returns a `Response`. The client code under test never knows the difference. That is the whole trick: **inject the client**, so tests can inject a fake one.

## Query parameters and routing in the fake

```python
import httpx

def handler(request: httpx.Request) -> httpx.Response:
    print(request.method, request.url.path, dict(request.url.params))
    if request.url.path == "/users":
        page = int(request.url.params.get("page", "1"))
        return httpx.Response(200, json={"page": page, "results": []})
    return httpx.Response(404, json={"error": "not found"})

client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")
print(client.get("/users", params={"page": 2}).json())
print(client.get("/nope").status_code)
```

Pass `params=` instead of gluing `?page=2` into the URL: httpx encodes it for you.

## Status codes are data

> **Predict first.** `client.get("/nope")` returned a 404. Did Python raise an exception?

No. A 404 is a *successful HTTP exchange* whose answer is "no". httpx only raises on transport problems, unless you ask:

```python
import httpx

client = httpx.Client(
    transport=httpx.MockTransport(lambda r: httpx.Response(500, json={"error": "boom"})),
    base_url="https://api.example.test",
)
resp = client.get("/x")
print(resp.status_code, resp.is_success, resp.json())
try:
    resp.raise_for_status()
except httpx.HTTPStatusError as exc:
    print("raised:", exc.response.status_code)
```

Rule of thumb: **2xx** success, **4xx** your request was wrong (don't retry blindly), **5xx** their problem (maybe retry), **429** slow down.

## Timeouts and transport errors

A call with no timeout can hang a pipeline forever. Always set one. Failures *before* a response exist raise subclasses of `httpx.TransportError`, such as `httpx.ConnectTimeout` or `httpx.ReadTimeout`. Our mock can raise them:

```python
import httpx

def handler(request: httpx.Request) -> httpx.Response:
    raise httpx.ReadTimeout("simulated slow server", request=request)

client = httpx.Client(
    transport=httpx.MockTransport(handler),
    base_url="https://api.example.test",
    timeout=httpx.Timeout(5.0, connect=2.0),
)
try:
    client.get("/slow")
except httpx.TimeoutException as exc:
    print("timed out:", type(exc).__name__)
```

Catch the **narrowest** class you can handle: `TimeoutException` for timeouts, `HTTPStatusError` for bad statuses, `HTTPError` as the umbrella for both.

## Sending JSON and headers

```python
import httpx

def handler(request: httpx.Request) -> httpx.Response:
    import json
    body = json.loads(request.content)
    return httpx.Response(201, json={"echo": body, "auth": request.headers.get("authorization")})

client = httpx.Client(
    transport=httpx.MockTransport(handler),
    base_url="https://api.example.test",
    headers={"Authorization": "Bearer demo-token"},
)
print(client.post("/events", json={"kind": "signup"}).json())
```

`json=` serialises the body and sets the content type. Client-level `headers=` apply to every call, a good home for auth.

## Structure the code for testing

```python
import httpx

def get_user_name(client: httpx.Client, user_id: int) -> str:
    resp = client.get(f"/users/{user_id}")
    resp.raise_for_status()
    return resp.json()["name"]

def fake(request):
    return httpx.Response(200, json={"id": 7, "name": "Grace"})

client = httpx.Client(transport=httpx.MockTransport(fake), base_url="https://api.example.test")
print(get_user_name(client, 7))
```

The function takes a `client` argument rather than creating one. In production you pass a real client; in tests a mock one.

## Common mistakes

- Treating a response as data without checking status. A 500 with a JSON error body parses fine and silently poisons your table.
- No timeout. The default is short but not infinite; set it explicitly and deliberately.
- Catching bare `Exception`, which hides bugs such as `KeyError` on a changed payload.
- Building URLs by string concatenation; a space or `&` in a value breaks it. Use `params=`.
- Constructing the client inside the function, which makes it impossible to test offline.
- `resp.json()` on an HTML error page raises `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. Check the status first.

## What to take away

1. A request is method + URL + headers + body; a response is status + headers + body.
2. 4xx/5xx are not exceptions until you call `raise_for_status()`.
3. Always set a timeout and catch the narrowest exception class that fits.
4. Pass the `httpx.Client` into your functions; tests inject `httpx.MockTransport`.
5. Use `params=` and `json=` rather than building strings by hand.
