`source_a` and `source_b` represent the same logical entity from two systems, but source_b's columns differ in name and type (amount_usd is a VARCHAR that needs casting to a DECIMAL, and it's named differently than amount). Combine both sources into consistent output columns `id`, `name`, `amount`, `created_at`, plus a literal `source_system` ('a' or 'b'). Then keep only the latest row per id (by created_at), in case the same id exists in both sources.

Return `id`, `name`, `amount`, `created_at`, `source_system`, ordered by `id`.
