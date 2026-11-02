Build the dict you would pass to `snowflake.connector.connect(**params)`. Write `build_params(env, secrets, job, run_id, *, allow_prod=False)`:

- start with the environment's `database`, `warehouse`, `role` (via the provided `environment_params`);
- add `account` and `user` from `secrets["SF_ACCOUNT"]` and `secrets["SF_USER"]` (a missing one raises `KeyError`);
- authentication: if `SF_PRIVATE_KEY_PATH` is in `secrets` add `authenticator="snowflake_jwt"` and `private_key_file=<path>`; elif `SF_PASSWORD` is there add `password`; else raise `ValueError` mentioning both names. The key pair wins if both exist;
- refuse automation roles: if the role is `ACCOUNTADMIN` or `SECURITYADMIN` (any case) raise `ValueError`;
- add `session_parameters={"QUERY_TAG": <compact JSON of {"job", "env", "run"}, sorted keys, separators (",", ":")>}`.

```python
build_params("dev", {"SF_ACCOUNT": "org-acct", "SF_USER": "SVC", "SF_PASSWORD": "x"}, "load_orders", "r1")
```
