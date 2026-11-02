Build the job's settings loader.

`Settings` is a pydantic model with fields `api_url: str`, `api_token` (a secret that must never appear in `repr()` or `str()` of the object), `timeout_s: float = 10.0`, `batch_size: int = 500`, `debug: bool = False`.

`load_settings(env)` reads variables named `APP_<FIELD>` in upper case (`APP_API_URL`, `APP_API_TOKEN`, `APP_TIMEOUT_S`, `APP_BATCH_SIZE`, `APP_DEBUG`) from the mapping `env`, ignores unrelated keys, and returns a `Settings`. If anything is missing or invalid it raises `ConfigError` whose message lists **every** offending variable name (e.g. `APP_API_TOKEN`), not just the first.

```python
s = load_settings({"APP_API_URL": "https://x.test", "APP_API_TOKEN": "s3cret", "APP_BATCH_SIZE": "250"})
s.batch_size                     # 250
"s3cret" in repr(s)              # False
s.api_token.get_secret_value()   # "s3cret"
```
