`raw_payloads.payload` is a JSON string -- the sandbox's analog to a Snowflake VARIANT column (which you'd normally access with `payload:plan::string`).

Return `id`, `account_id`, and the extracted `plan` value from the payload.

Order by `id`.
