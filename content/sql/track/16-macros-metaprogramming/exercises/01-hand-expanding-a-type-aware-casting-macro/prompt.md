This repo's staging_model_generator macro loops over a list of source columns and emits type-aware casts (e.g. TIMESTAMP columns get an explicit ::varchar cast; everything else passes through).

Hand-expand what that macro would generate for `source_a` (columns: id, name, amount, created_at): cast created_at to VARCHAR, and leave id, name, amount as-is.

Return `id`, `name`, `amount`, `created_at` (as VARCHAR), ordered by `id`.
