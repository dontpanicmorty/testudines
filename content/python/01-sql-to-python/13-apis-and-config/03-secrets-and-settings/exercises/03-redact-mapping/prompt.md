A job logs its connection parameters when it starts, and the password ends up in the log aggregator. Finish `redact(data)`.

It returns a **new** structure where the value of any dict key containing `password`, `secret`, `token`, `key` or `authorization` (case-insensitive) is replaced by the string `"***"`. It must recurse into nested dicts and into lists/tuples of dicts. Other values are unchanged and the original input is never modified. At the moment secrets inside nested dicts leak.

```python
redact({"user": "svc", "password": "p", "opts": {"api_token": "t", "region": "eu"}})
# {"user": "svc", "password": "***", "opts": {"api_token": "***", "region": "eu"}}
```
