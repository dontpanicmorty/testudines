`source_a` and `source_b` represent the same logical entity from two systems, but source_b's columns differ in name and type (amount_usd is a VARCHAR that needs casting to a DECIMAL, and it's named differently than amount).

Similar to this repo's gainsight_union_relations macro (which force-casts mismatched columns before a UNION), write a query combining both sources into consistent output columns `id`, `name`, `amount`, `created_at`, plus a literal `source_system` ('a' or 'b').

Order by `id`, then `source_system`.
